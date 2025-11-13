import pandas as pd
from nameparser import HumanName
from collections import Counter
from constants import *
import re


def remove_suffixes(df):
    def strip_name(name):
        if pd.isna(name):
            return name
        clean = re.sub(r'(["\']).*?\1', '', name)
        hn = HumanName(clean)
        hn.suffix = ''
        return str(hn).strip()
    df['tempName'] = df['Name'].apply(strip_name)
    return df

def insert_chair_peek(df, final):
    """If the row immediately before the first final index is a chair role, prepend its index."""
    if not final:
        return

    first_idx = min(final)
    peek_idx  = first_idx - 1

    if peek_idx not in df.index:
        return

    pos = str(df.at[peek_idx, "Position"]).lower().strip()
    if pos in {"chairman", "chairperson", "chair"} and peek_idx not in final:
        final.insert(0, peek_idx)

def get_board_names(df):
    """
    Infer each institution’s board keyword by sampling its last 10 positions.
    Applies a governor/director vs trustee/regent runner‑up override.
    """
    board_names = {}
    for institution, group in df.groupby('Institution'):
        recent = group.tail(10)['Position'].dropna().astype(str)
        counts = Counter()
        for pos in recent:
            pl = pos.lower()
            for word in POSITION_BANK:
                if word.lower() in pl and 'director, ' not in pl:
                    counts[word] += 1
        chosen = None
        if counts:
            common = counts.most_common()
            top_word, top_count = common[0]
            if len(common) > 1:
                second_word, second_count = common[1]
                if (top_word.lower() in {'governor','director'}
                    and second_word.lower() in {'trustee','regent'}
                    and second_count >= 0.8 * top_count):
                    top_word = second_word
            if top_word in BOARD_WORDS:
                chosen = top_word
        board_names[institution] = chosen
    return board_names

def detect_director_boards(df, board_names):
    """
    Institutions without board_names whose last 10 positions
    are most commonly exactly 'director'. Prints detections.
    """
    director_institutions = set()
    for institution, group in df.groupby('Institution'):
        if board_names.get(institution):
            continue
        recent = group.tail(10)['Position'].fillna('').astype(str)
        counts = Counter(
            p.lower().strip()
            for p in recent
            if p.strip() and not ('director' in p.lower() and 'director,' in p.lower())
        )
        most_common = counts.most_common(2)
        if len(most_common) > 1:
            second_most_common_key = most_common[1][0]
        else:
            second_most_common_key = None
        if counts and counts.most_common(1)[0][0] == 'director' and second_most_common_key != 'dean' and counts.most_common(1)[0][1] > 3:
            # print(f'Director board detected for {institution}')
            director_institutions.add(institution)
    return director_institutions


def get_permissive_blocks(df, board_names):
    '''Create blocks of boards of directors with some exceptions that can be deleted in second scan'''
    #lots of rules that need to be added due to odd ways some schools report or minor OCR artifacts
    static_exceptions = ['secretary','chairman','treasurer','chairperson','vice chair', 'member']
    blocks = {}
    all_BOARD_WORDS = set(BOARD_WORDS)
    #go through all schools
    for institution, group in df.groupby('Institution'):
        names = group['tempName'].dropna().astype(str).tolist()
        last_names = [n.split()[-1].lower() for n in names]
        positions = group['Position'].fillna('').astype(str).tolist()
        indices = group.index.to_list()

        board_word = (board_names.get(institution) or '').lower()
        others = all_BOARD_WORDS - {board_word.title()}
        # precompute how often each "other" appears in this group
        other_freq = {other: sum(1 for p in positions if other.lower() in p.lower())for other in others}
        board_freq = sum(1 for p in positions if board_word in p.lower())

        #start at the last occurrence of the board word (makes expanding board upward more reliable)
        if board_word:
            matches = [i for i, p in enumerate(positions) if board_word in p.lower()]
            if matches:
                start_idx = matches[-1]
            else:
                start_idx = len(last_names) - 1
        else:
            start_idx = len(last_names) - 1

        #expand board upward from starting position
        i = start_idx - 1
        while i >= 0:
            p_lower = positions[i].lower()
            #For inst with 2 boards, stop expanding upward if that board is reached
            hit_other = False
            for other in others:
                if other.lower() in p_lower and other_freq.get(other, 0) > (1/3) * board_freq and other.lower() != 'member' :
                    hit_other = True
                    i = -1
                    break
            if hit_other or i < 0:
                break

            #things to check while expanding up
            in_order = last_names[i] <= last_names[i+1]
            is_board = board_word in p_lower
            is_exception = any(exc in p_lower for exc in static_exceptions)

            #checks pass
            if in_order or is_board or is_exception:
                start_idx = i
                i -= 1
                continue
            #shorthand
            if last_names[i].startswith(('a')):
                break

            successes = 0
            peeks = 0
            #can peek up to account for previous checks failing
            for j in range(i-1, max(i-4, -1), -1):
                peeks += 1
                pj = positions[j].lower()
            
                if 'dean' in pj or ('director' in pj and board_word != 'director') or 'director,' in pj:
                    continue
                j_in_order = last_names[j] <= last_names[j+1]
                j_is_board = board_word in pj
                j_is_exception = any(exc in pj for exc in static_exceptions)

                # if j_in_order or j_is_board or j_is_exception:
                if j_is_board or (j_in_order and j_is_exception):
                    successes += 1
            #require certain number of correct board members when peeking upward
            if peeks >= 2 and successes >= 2:
                start_idx = i
                i -= 1
                continue
            else:
                break

        blocks[institution] = indices[start_idx:]
    return blocks


def split_into_contiguous_runs(indices):
    #boards are reported in one block, so if there are gaps, there is an issue
    if not indices:
        return []
    sorted_idx = sorted(indices)
    runs = [[sorted_idx[0]]]
    for x in sorted_idx[1:]:
        if x == runs[-1][-1] + 1:
            runs[-1].append(x)
        else:
            runs.append([x])
    return runs



def mark_board_members(df, board_names):
    '''mark the boards of each institution (if exists)'''
    static_exc = ['secretary','chairman','treasurer','chairperson']
    #When the board is called 'director', this is a special case
    director_insts = detect_director_boards(df, board_names)
    names_map = board_names.copy()

    for inst in director_insts:
        names_map[inst] = 'director'

    #get blocks of boards and iterate through them, marking the true start/ends
    blocks = get_permissive_blocks(df, names_map)
    validated_idx = []
    for inst, idx_list in blocks.items():
        board_word = (names_map.get(inst) or '').lower()
        if not board_word or not idx_list:
            continue

        #list of exception words which are titles that are contained within the osition block
        dyn_exc = {str(df.at[i,'Position']).lower().strip() for i in idx_list if 'dean' not in str(df.at[i,'Position']).lower()}
        exceptions = set(static_exc) | dyn_exc

        #find first occurrence of the board keyword and record index within the block
        first_rel = None
        for rel, i in enumerate(idx_list[:10]):
            p = str(df.at[i,'Position']).lower().strip()
            if (board_word == 'director' and p == 'director') or (board_word != 'director' and board_word in p):
                first_rel = rel
                break
        if first_rel is None:
            continue
        #expand up to 3 rows above for exceptions
        window = 3
        start_rel = max(0, first_rel - window)
        earliest = first_rel
        for rel in range(start_rel, first_rel):
            if any(exc in str(df.at[idx_list[rel],'Position']).lower() for exc in exceptions):
                earliest = rel
                break
        selected = idx_list[earliest:]

        #ensure that the blocks are contiguous
        runs = split_into_contiguous_runs(selected)
        longest = max(runs, key=len)
        kept = [longest]
        for run in runs:
            if run is longest:
                continue
            if len(run) <= 2:
                continue
            gap = (run[0] - longest[-1] - 1
                   if run[0] > longest[-1]
                   else longest[0] - run[-1] - 1)
            if gap > 25:
                continue
            kept.append(run)

        #flatten into final index list
        final = [i for r in kept for i in r]
        #peek above the last marked row for a chairman incase this was missed in the expansion
        insert_chair_peek(df, final)
        validated_idx.extend(final)
        df.loc[final, 'FixedPosition'] = 'Board Member'
    board_df = df.loc[validated_idx].copy()
    df = df.drop(columns='tempName', errors='ignore')
    board_df = board_df.drop(columns='tempName', errors='ignore')
    return df, board_df

def detect_primary_and_secondary_boards(df):
    board_names_1 = get_board_names(df)
    df_labeled, board_df_1 = mark_board_members(df.copy(), board_names_1)

    remaining = df.drop(index=board_df_1.index)
    board_names_2 = get_board_names(remaining)
    _, board_df_2= mark_board_members(remaining.copy(), board_names_2)

    # if no second board, we’re done
    if board_df_2.empty:
        return df_labeled, board_df_1

    # (mark_board_members already set FixedPosition='Board Member' on df_labeled)
    df_labeled.loc[board_df_2.index, 'FixedPosition'] = 'Second Board Member'
    board_df_1 = board_df_1.assign(FixedPosition='Board Member')
    board_df_2 = board_df_2.assign(FixedPosition='Second Board Member')

    for inst in board_df_2['Institution'].unique():
        # exact-match selection
        idx1 = board_df_1.loc[board_df_1['Institution'] == inst].index
        idx2 = board_df_2.loc[board_df_2['Institution'] == inst].index

        if not idx1.empty and not idx2.empty:
            #right now, using the smaller board as the main one (voting board)
            if len(idx1) > len(idx2):
                # swap them
                df_labeled.loc[idx1, 'FixedPosition'] = 'Second Board Member'
                df_labeled.loc[idx2, 'FixedPosition'] = 'Board Member'
                board_df_1.loc[idx1, 'FixedPosition']  = 'Second Board Member'
                board_df_2.loc[idx2, 'FixedPosition']  = 'Board Member'

    combined = pd.concat([board_df_1, board_df_2], axis=0)
    return df_labeled, combined


def clean_and_report_boards(df_labeled, board_df):
    '''Drop leading rows if they have dean or director'''
    df_clean = df_labeled.copy()
    bd_clean = board_df.copy()

    for inst in sorted(bd_clean['Institution'].unique()):
        for label in ['Board Member', 'Second Board Member']:
            mask = (bd_clean['Institution'] == inst) & (bd_clean['FixedPosition'] == label)
            inst_rows = bd_clean[mask].sort_index()
            if inst_rows.empty:
                continue

            pos_series = inst_rows['Position'].astype(str).str.lower()
            #strip off leading 'dean' or 'director,'
            to_drop = []
            for idx, p in pos_series.items():
                if 'dean' in p or 'director,' in p:
                    to_drop.append(idx)
                else:
                    break

            if to_drop:
                df_clean = df_clean.drop(index=to_drop)
                bd_clean = bd_clean.drop(index=to_drop)
                # refresh pos_series after dropping
                mask = (bd_clean['Institution'] == inst) & (bd_clean['FixedPosition'] == label)
                inst_rows = bd_clean[mask].sort_index()
                pos_series = inst_rows['Position'].astype(str).str.lower()

    return df_clean, bd_clean

def process_boards(full_df):
    """
    Remove suffixes from the full dataframe, detect primary and secondary boards,
    then clean and report on those boards. Returns the updated full_df and board_df.
    """
    full_df = remove_suffixes(full_df)
    full_df, board_df = detect_primary_and_secondary_boards(full_df)
    full_df, board_df = clean_and_report_boards(full_df, board_df)
    return full_df, board_df