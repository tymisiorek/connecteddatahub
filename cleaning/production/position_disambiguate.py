import pandas as pd
import numpy as np
import os
from collections import Counter
import re
from collections import defaultdict
from nameparser import HumanName
from constants import *


def assign_position_grouping_subinst(position, s):
    """Classify a position string using keywords and an arbitrary trigger substring."""
    classification = ""
    for key, value in KEYWORDS.items():
        variants = [s.title() for s in value]
        found_variant = any(v in position for v in variants)

        idx = position.rfind(s)
        if idx != -1:
            after = position[idx + len(s) :].strip()
        else:
            after = ""

        if key.title() == after or found_variant:
            classification += key + ", "

    return classification.strip(", ")


'''President Functions'''
def mark_president_positions(df):
    if "FixedPosition" not in df.columns:
        df["FixedPosition"] = pd.Series([None] * len(df), index=df.index, dtype="object")
    else:
        df["FixedPosition"] = df["FixedPosition"].astype("object")

    def is_true_president(pos):
        pos = str(pos).lower()
        return any(p in pos for p in PRESIDENT_WORDS) and "vice" not in pos

    president_indices = []
    found_late = []   
    not_found = []

    for inst, group in df.groupby("Institution", sort=False):
        idxs = list(group.index)
        # check first row
        first_idx = idxs[0]
        if is_true_president(df.at[first_idx, "Position"]):
            president_indices.append(first_idx)
            continue
        # look in the next up to 3 rows
        found = False
        for nxt in idxs[1:4]:
            if is_true_president(df.at[nxt, "Position"]):
                president_indices.append(nxt)
                found_late.append((inst, nxt, df.at[nxt, "Position"]))
                found = True
                break
        if not found:
            seen_positions = [str(df.at[i, "Position"]).strip() for i in idxs[:4]]
            not_found.append((inst, seen_positions))
    df.loc[president_indices, "FixedPosition"] = "President"
    president_rows = df.loc[president_indices].copy()

    return df, president_rows



'''Provost Functions'''
def mark_first_provost_positions(df):
    """Mark the first acceptable 'Provost' per institution, return a solely provost df and the original df with an updated 'FixedPosition' column"""
    if "FixedPosition" not in df.columns:
        df["FixedPosition"] = np.nan

    accepted_indices = []

    for inst, group in df.groupby("Institution"):
        for idx, row in group.iterrows():
            pos = str(row["Position"]).strip()
            pos_lower = pos.lower()
            if "provost" in pos_lower and not any(bad in pos_lower for bad in ["vice", "assistant", "associate", ","]):
                accepted_indices.append(idx)
                break

    df.loc[accepted_indices, "FixedPosition"] = "Provost"
    df.loc[accepted_indices, "Designation"] = "Head Provost"
    provost_rows = df.loc[accepted_indices].copy()

    return df, provost_rows

def extract_all_provost(df):
    mask = df['Position'].str.contains("Provost", case=False, na=False)
    provost_df = df.loc[mask].copy()
    return pd.DataFrame(provost_df)


def check_provost_keyword(row):
    """Classify what type of provost"""
    pos = row["Position"].title()
    inst = row["Institution"].title()
    subinst = row["SubInstitution"]
    blank = pd.isna(subinst)

    lower = pos.lower()
    idx = lower.find("provost")
    provost_type = pos[idx + len("provost"):].strip() if idx >= 0 else ""

    matches = []
    for key, keywords in VP_KEYWORDS.items():
        for kw in keywords:
            if kw.title() in pos and "director, " not in lower:
                matches.append(key)
                break
    if matches:
        return ", ".join(matches)

    generic_titles = {
        "Provost",
        "Executive Provost",
        "Head Provost",
        "Chief Provost",
    }
    if pos in generic_titles:
        return "Generic" if blank else "SubInstitution"

    if blank and (provost_type == "" or ("," not in pos and "." not in pos)):
        return "Generic"

    if inst in pos and "Foundation" not in pos:
        return "Satellite Campus"
    return ""


def classify_provost(df):
    out = df.copy()
    out["FixedPosition"] = out.apply(check_provost_keyword, axis=1)
    return out


def remaining_classification_provost(provost_df):
    for index, row in provost_df.iterrows():
        current = row["FixedPosition"]
        is_blank = current == ""
        position = row["Position"].title()
        if "Campus" in position and is_blank:
            provost_df.at[index, "FixedPosition"] += "Satellite Campus, "
        if "Academic" in position and is_blank:
            provost_df.at[index, "FixedPosition"] += "Academic Affairs, "
        if "Administration" in position and is_blank:
            provost_df.at[index, "FixedPosition"] += "Administration, "
        if ("Development" in position or "Advancement" in position) and is_blank:
            provost_df.at[index, "FixedPosition"] += "Advancement, "
        if current == "" and "Campus" in position:
            provost_df.at[index, "FixedPosition"] = "Satellite Campus"
        elif current == "":
            provost_df.at[index, "FixedPosition"] = "Other"
        provost_df.at[index, "FixedPosition"] = provost_df.at[index, "FixedPosition"].rstrip(", ")
    return provost_df


def classify_subinstitution_provost(provost_df, grouped_df):
    subinstitution_dict = grouped_df.set_index(["Institution", "SubInstitution"])["Category"].to_dict()
    df = provost_df.copy()
    df["PositionTitle"] = df["Position"].str.title()
    df["provost_index"] = df["Position"].str.rfind("Provost") + len("Provost")

    df["Category"] = df.set_index(
        ["Institution", "SubInstitution"]
    ).index.map(subinstitution_dict)

    mask_a = (
        df["FixedPosition"].str.contains("SubInstitution|Other", na=False)
        & df["SubInstitution"].notna()
        & (df["provost_index"] == df["PositionTitle"].str.len())
    )
    df.loc[mask_a, "FixedPosition"] = df.loc[mask_a, "Category"].where(
        df.loc[mask_a, "Category"] != "Error", other="Generic"
    )

    mask_b = (
        df["FixedPosition"].str.contains("SubInstitution", na=False)
        & (df["provost_index"] != df["PositionTitle"].str.len())
    )
    df.loc[mask_b, "FixedPosition"] = df.loc[mask_b, "PositionTitle"].apply(
        lambda pos: assign_position_grouping_subinst(pos, "Provost,")
    )

    mask_c = (
        (df["provost_index"] != df["PositionTitle"].str.len())
        & df["SubInstitution"].isna()
        & df["FixedPosition"].str.contains("Other", na=False)
    )
    def classify_or_other(pos):
        c = assign_position_grouping_subinst(pos, "Provost,")
        return c if c else "Other"
    df.loc[mask_c, "FixedPosition"] = df.loc[mask_c, "PositionTitle"].apply(classify_or_other)

    mask_other = df["FixedPosition"] == "Other"
    df.loc[mask_other, "FixedPosition"] = df.loc[mask_other, "PositionTitle"].apply(classify_or_other)

    return df.drop(columns=["PositionTitle", "provost_index", "Category"])



'''Board Functions'''
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
    board_names_1        = get_board_names(df)
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



'''Vice President Functions'''
def extract_all_vp(df):
    mask = df['Position'].str.contains("Vice President", case=False, na=False)
    vp_df = df.loc[mask].copy()
    return pd.DataFrame(vp_df)


def check_keyword(row):
    #classify what type of vice president
    pos = row["Position"].title()
    inst = row["Institution"].title()
    subinst = row["SubInstitution"]
    blank = pd.isna(subinst)

    #Precompute the “vice president” suffix (e.g. “Of Finance” in “Vice President Of Finance”)
    lower = pos.lower()
    idx = lower.find("vice president")
    vp_type = pos[idx + len("vice president"):].strip() if idx >= 0 else ""

    matches = []
    for key, keywords in VP_KEYWORDS.items():
        for kw in keywords:
            if kw.title() in pos and "director, " not in lower:
                matches.append(key)
                break 
    if matches:
        return ", ".join(matches)

    generic_titles = {"Vice President","Executive Vice President","Head Vice President","Chief Vice President",}
    if pos in generic_titles:
        return "Generic" if blank else "SubInstitution"

    #Blank + no suffix + no punctuation = Generic
    if blank and (vp_type == "" or ("," not in pos and "." not in pos)):
        return "Generic"

    #Institution name inside title (but not “Foundation”) = Satellite Campus
    if inst in pos and "Foundation" not in pos:
        return "Satellite Campus"
    return ""


def classify_vp(df):
    out = df.copy()
    out['FixedPosition'] = out.apply(check_keyword, axis=1)
    return out

def remaining_classification(vp_df):
    for index, row in vp_df.iterrows():
        type = row['FixedPosition']
        type_blank = False
        if type == "":
            type_blank = True
        position = row["Position"].title()
        if "Campus" in position and type_blank == True:
            vp_df.at[index, 'FixedPosition'] += "Satellite Campus, "
        if "Academic" in position and type_blank == True:
            vp_df.at[index,'FixedPosition'] += "Academic Affairs, "
        if "Administration" in position and type_blank == True:
            vp_df.at[index, 'FixedPosition'] += "Administration, "
        if ("Development" in position or "Advancement" in position) and type_blank == True:
            vp_df.at[index, 'FixedPosition'] += "Advancement, "
        if type == "" and "Campus" in position:
            vp_df.at[index, 'FixedPosition'] = "Satellite Campus"
        elif type == "":
            vp_df.at[index, 'FixedPosition'] = "Other"
        vp_df.at[index, 'FixedPosition'] = vp_df.at[index, 'FixedPosition'].rstrip(", ")
    return vp_df



def classify_subinstitution_vp(vp_df, grouped_df):
    subinstitution_dict = grouped_df.set_index(['Institution', 'SubInstitution'])['Category'].to_dict()
    df = vp_df.copy()
    df['PositionTitle'] = df['Position'].str.title()
    # +14 yields e.g. 13 if 'Vice President' ends at idx -1+14
    df['vp_index'] = df['Position'].str.rfind('Vice President') + 14

    df['Category'] = df.set_index(['Institution', 'SubInstitution']).index.map(subinstitution_dict)
    #SubInstitution or Other in FixedPosition,
    mask_a = (df['FixedPosition'].str.contains('SubInstitution|Other', na=False) & df['SubInstitution'].notna() & (df['vp_index'] == df['PositionTitle'].str.len()))
    df.loc[mask_a, 'FixedPosition'] = df.loc[mask_a, 'Category'].where(df.loc[mask_a, 'Category'] != 'Error', other='Generic')

    #still contains "SubInstitution", but vp_index != full length
    mask_b = (df['FixedPosition'].str.contains('SubInstitution', na=False) & (df['vp_index'] != df['PositionTitle'].str.len()))
    df.loc[mask_b, 'FixedPosition'] = df.loc[mask_b, 'PositionTitle'].apply(lambda pos: assign_position_grouping_subinst(pos, 'Vice President,'))

    #vp_index != full length, SubInstitution is NaN, and "Other" in FixedPosition
    mask_c = ((df['vp_index'] != df['PositionTitle'].str.len()) & df['SubInstitution'].isna() & df['FixedPosition'].str.contains('Other', na=False))

    def classify_or_other(pos):
        c = assign_position_grouping_subinst(pos, 'Vice President,')
        return c if c else 'Other'
    
    df.loc[mask_c, 'FixedPosition'] = df.loc[mask_c, 'PositionTitle'].apply(classify_or_other)
    mask_other = df['FixedPosition'] == 'Other'
    df.loc[mask_other, 'FixedPosition'] = df.loc[mask_other, 'PositionTitle'].apply(classify_or_other)
    df = df.drop(columns=['PositionTitle', 'vp_index', 'Category'])
    return df

def last_sweep(df):
    out = df.copy()
    out['FixedPosition'] = out['FixedPosition'].fillna("").replace("", "Other")
    return out

def add_seniority(vp_df):
    df = vp_df.copy()
    pos_lc = df['Position'].fillna("").str.lower()
    df['Seniority'] = "Default"
    mask = pos_lc.str.contains(r"\bassistant\b")
    df.loc[mask, 'Seniority'] = "Assistant"
    mask = pos_lc.str.contains(r"\bassociate\b")
    df.loc[mask, 'Seniority'] = "Associate"
    mask = pos_lc.str.contains(r"\bsenior\b")
    df.loc[mask, 'Seniority'] = "Senior"
    mask = pos_lc.str.contains(r"\bexecutive\b")
    df.loc[mask, 'Seniority'] = "Executive"
    return df


'''Deans Functions'''
def extract_deans(df):
    pos = df['Position'].fillna("").str.lower()
    mask = pos.str.contains(r'dean') & ~pos.str.contains(r'assistant to the dean')
    return df.loc[mask].copy()

#remove parentheses at end of string *used for Dean (interim) or Dean (acting)
def remove_parentheses(string):
    index = string.find('(')
    if index != -1:
        string = string[:index]
    return string.title()

def assign_position_grouping(position):
    classification = ""
    for key, value in DEAN_KEYWORDS.items():
        value_upper = [s.title() for s in value]
        keyword_appears = any(s in position for s in value_upper)
        dean_comma = position.rfind("Dean,") + 5
        if key.title() == position[dean_comma:]:
            classification += key + ", "
        elif keyword_appears:
            classification += key + ", "
    return classification.strip(", ")

def assign_deans_subinstitution(deans_df, subinstitution_df):
    # start fresh
    deans_df["FixedPosition"] = ""

    # lookup: (Institution, SubInstitution) → Category
    subinst_cat = (
        subinstitution_df
        .set_index(["Institution", "SubInstitution"])["Category"]
        .to_dict()
    )

    # pre-compute helpers
    pos_title = deans_df["Position"].fillna("").astype(str).str.title()
    altered = pos_title.apply(remove_parentheses).str.strip()
    dean_idx = altered.str.rfind("Dean") + 4
    altered_len = altered.str.len()

    has_sub = deans_df["SubInstitution"].notna()

    mask = (dean_idx == altered_len) & has_sub
    keys = list(zip(
        deans_df.loc[mask, "Institution"],
        deans_df.loc[mask, "SubInstitution"]
    ))
    deans_df.loc[mask, "FixedPosition"] = (
        pd.Series(keys, index=deans_df.index[mask])
          .map(subinst_cat)
    )

    mask = (dean_idx == altered_len) & ~has_sub
    deans_df.loc[mask, "FixedPosition"] = "Generic"

    mask = (dean_idx != altered_len) & has_sub
    deans_df.loc[mask, "FixedPosition"] = pos_title[mask].apply(lambda pos: assign_position_grouping_subinst(pos, "Dean,"))

    mask = (dean_idx != altered_len) & ~has_sub
    deans_df.loc[mask, "FixedPosition"] = pos_title[mask].apply(lambda pos: assign_position_grouping_subinst(pos, "Dean,"))

    return deans_df

def assign_remaining(deans_df, subinstitution_df):
    df = deans_df.copy()
    # helpers
    pos_title = df["Position"].fillna("").astype(str).str.title()
    altered = pos_title.apply(remove_parentheses).str.strip()
    dean_idx = altered.str.rfind("Dean") + 4
    pos_len = pos_title.str.len()

    # 1) rows whose FixedPosition was originally blank
    mask_empty = df["FixedPosition"] == ""
    df.loc[mask_empty, 'FixedPosition'] = (
        pos_title[mask_empty]
        .apply(lambda p: assign_position_grouping_subinst(p, 'Dean,'))
    )


    # 2) same blank rows where "Dean" ends the string
    mask_end = mask_empty & (dean_idx == pos_len)
    df.loc[mask_end, "FixedPosition"] = "Generic"

    # 3) any row whose Position already contains that phrase
    mask_phrase = pos_title.str.contains("Dean Of The College", na=False)
    df.loc[mask_phrase, "FixedPosition"] = "Generic"

    return df


def assign_none(deans_df):
    mask = deans_df['FixedPosition'] == ''
    deans_df.loc[mask, 'FixedPosition'] = 'Administration'
    return deans_df


def assign_administration(deans_df):
    pattern = '|'.join(map(re.escape, ADMIN_TYPES))
    mask = deans_df['FixedPosition'].str.contains(pattern, na=False)
    deans_df.loc[mask, 'FixedPosition'] = 'Administration'
    return deans_df


def process_matches(deans_df):
    mask = deans_df['FixedPosition'].str.contains('Subinstitution Match', na=False)
    deans_df.loc[mask, 'FixedPosition'] = (
    deans_df.loc[mask, 'Position'].apply(lambda p: assign_position_grouping_subinst(p, 'Dean,')))

    return deans_df


def cleanup(deans_df):
    cleanup_list = [
        "Faculty", "Administrator", "Students", "Administrative", "Enrollment",
        "Finance", "Foundation", "Student", "Academic Affair", "Programs",
        "Alumni", "Relations", "Conservatory", "Division", "Professions",
        "Practice", "Educational", "Office", "Management"
    ]
    # build a single OR-pattern, escaping any regex metacharacters
    pattern = '|'.join(map(re.escape, cleanup_list))

    # ── pre-compute helpers ──────────────────────────────────────────────
    pos_title = deans_df['Position'].fillna('').astype(str).str.title()
    altered   = pos_title.apply(remove_parentheses).str.strip()
    dean_idx  = altered.str.rfind('Dean') + 4
    not_at_end = dean_idx != altered.str.len()

    sub_title = deans_df['SubInstitution'].fillna('').astype(str).str.title()

    # does Position or SubInstitution contain a cleanup keyword?
    pos_hit = pos_title.str.contains(pattern, na=False)
    sub_hit = sub_title.str.contains(pattern, na=False)

    # rows to re-label
    mask = (
        not_at_end &
        (pos_hit | sub_hit) &
        (deans_df['FixedPosition'] != 'Administration')
    )

    deans_df.loc[mask, 'FixedPosition'] = 'Administration'
    return deans_df
        

def expand_grouping(deans_df, subinstitution_df):
    df = deans_df.copy()
    subinst_cat = subinstitution_df.set_index(
        ['Institution', 'SubInstitution'])['Category'].to_dict()

    sub_title   = df['SubInstitution'].fillna("").astype(str).str.title()
    pos_title   = df['Position'].fillna("").astype(str).str.title()

    keys = list(zip(df['Institution'], df['SubInstitution']))
    cat_series = pd.Series(keys, index=df.index).map(subinst_cat)
    key_str = df['Institution'].fillna("").astype(str) + df['SubInstitution'].fillna("").astype(str)
    fixed = df['FixedPosition']

    mask_grad = fixed.str.contains('Graduate', na=False) & (sub_title != "")
    df.loc[mask_grad, 'FixedPosition'] = cat_series[mask_grad]

    mask_grad_append = mask_grad & cat_series.notna() & ~cat_series.str.contains('Graduate', na=False)
    df.loc[mask_grad_append, 'FixedPosition'] = df.loc[mask_grad_append, 'FixedPosition'] + ', Graduate'


    mask_sat = sub_title.str.contains('Satellite Campus', na=False)
    df.loc[mask_sat, 'FixedPosition'] = df.loc[mask_sat, 'FixedPosition'] + ', Satellite Campus'

    mask_lib = pos_title.str.contains('Librar', na=False) & \
               ~key_str.str.contains('Information', case=False, na=False)
    df.loc[mask_lib, 'FixedPosition'] = 'Administration'


    mask_cont = pos_title.str.contains('Continu', na=False)
    df.loc[mask_cont, 'FixedPosition'] = 'Continued Studies'

    return df

def clean_fixed_positions(deans_df: pd.DataFrame) -> pd.DataFrame:
    """
    Collapse any runs of consecutive commas in the FixedPosition column.
    """
    # identify rows where FixedPosition contains at least two commas in a row
    mask = deans_df['FixedPosition'].str.contains(',,', na=False)
    # perform a regex replace equivalent to remove_consecutive_commas
    deans_df.loc[mask, 'FixedPosition'] = (
        deans_df.loc[mask, 'FixedPosition']
              .str.replace(r', ,+', ',', regex=True)
    )
    return deans_df
        


def categorize_subinstitutions(df):
    subinst = df['SubInstitution'].fillna('').str.title()
    fixed = df['FixedPosition']

    mask_arts = subinst.str.contains('Arts,', na=False) & ~fixed.str.contains('Arts and Sciences|Liberal Arts|Fine Arts', na=False)
    df.loc[mask_arts, 'FixedPosition'] = fixed[mask_arts] + ', Fine Arts'

    mask_natsci = subinst.str.contains('And Science', na=False) & ~fixed.str.contains('Arts and Sciences|Natural Sciences', na=False)
    df.loc[mask_natsci, 'FixedPosition'] = fixed[mask_natsci] + ', Natural Sciences'

    mask_libarts = fixed.str.contains('Liberal Arts', na=False) & fixed.str.contains('Arts and Sciences', na=False)
    df.loc[mask_libarts, 'FixedPosition'] = fixed[mask_libarts].str.replace('Liberal Arts', '', regex=False).str.strip(', ')

    eng_count = subinst.str.count(r'\bEngineering\b')
    mask_softeng = subinst.str.contains('Software Engineering', na=False) & fixed.str.contains('Engineering', na=False) & (eng_count == 1)
    df.loc[mask_softeng, 'FixedPosition'] = fixed[mask_softeng].str.replace('Engineering', '', regex=False).str.strip(', ')

    mask_hosp = subinst.str.contains('Hospitality', na=False) & fixed.str.contains('Hospital', na=False)
    df.loc[mask_hosp, 'FixedPosition'] = fixed[mask_hosp].str.replace('Hospital,', '', regex=False).str.strip(', ')

    mask_found = subinst.str.contains('Foundation School', na=False)
    df.loc[mask_found, 'FixedPosition'] = fixed[mask_found].str.replace('Foundation', '', regex=False).str.strip(', ')

    return df

'''individual pipelines'''

def process_presidents(full_df):
    return mark_president_positions(full_df)

def process_provost(full_df, grouped_df):
    mask = full_df['Position'].str.contains(r'Provost', case=False, na=False)
    provost_df = full_df.loc[mask].copy()

    # identify and mark head provosts
    temp_df, head_provost_df = mark_first_provost_positions(provost_df.copy())

    # run the normal provost pipeline on all provost rows
    provost_df = classify_provost(provost_df)
    provost_df = remaining_classification_provost(provost_df)
    provost_df = classify_subinstitution_provost(provost_df, grouped_df)
    provost_df = last_sweep(provost_df)
    provost_df = add_seniority(provost_df)

    # set Designation and reset FixedPosition label
    provost_df['Designation'] = provost_df['FixedPosition']
    provost_df['FixedPosition'] = 'Provost'

    # prepend "Vice " to FixedPosition where Position contains "Vice"
    # prepend "Vice " only on those rows that actually have "Vice" in Position
    vm = provost_df['Position'].str.contains('Vice', case=False, na=False)
    provost_df.loc[vm, 'FixedPosition'] = (
        'Vice ' + provost_df.loc[vm, 'FixedPosition']
    )


    # overwrite with head provost rows where applicable
    provost_df.loc[
        head_provost_df.index,
        ['FixedPosition', 'Designation']
    ] = head_provost_df[['FixedPosition', 'Designation']]

    # if head_provost_df contains a Seniority column, bring it across
    full_df.loc[mask, 'Seniority'] = provost_df['Seniority']
    # write back into the full_df
    full_df.loc[mask, ['FixedPosition', 'Designation', 'Seniority']] = provost_df[[
        'FixedPosition', 'Designation', 'Seniority'
    ]]
    return full_df, provost_df


def process_boards(full_df):
    """
    Remove suffixes from the full dataframe, detect primary and secondary boards,
    then clean and report on those boards. Returns the updated full_df and board_df.
    """
    full_df = remove_suffixes(full_df)
    full_df, board_df = detect_primary_and_secondary_boards(full_df)
    full_df, board_df = clean_and_report_boards(full_df, board_df)
    return full_df, board_df


def process_vice_presidents(full_df, grouped_df):
    """
    Extract and classify all Vice President rows, update full_df, and return both full_df and vp_df.
    """
    mask = full_df['Position'].str.contains(r'Vice President', case=False, na=False)
    vp_df = full_df.loc[mask].copy()

    vp_df = classify_vp(vp_df)
    vp_df = remaining_classification(vp_df)
    vp_df = classify_subinstitution_vp(vp_df, grouped_df)
    vp_df = last_sweep(vp_df)
    vp_df = add_seniority(vp_df)

    vp_df['Designation']   = vp_df['FixedPosition']
    vp_df['FixedPosition'] = 'Vice President'

    full_df.loc[mask, ['FixedPosition', 'Designation']] = vp_df[['FixedPosition', 'Designation']]
    full_df.loc[mask, 'Seniority'] = vp_df['Seniority']

    return full_df, vp_df

def process_deans(full_df, subinstitution_df):
    """
    Extract and classify all Dean rows, update full_df, and return both full_df and dean_df.
    """
    dean_mask = (
        full_df["Position"].str.contains(r"\bDean\b", case=False, na=False)
        & ~full_df["Position"].str.contains(r"Assistant to the Dean", case=False, na=False)
    )
    dean_df = full_df.loc[dean_mask].copy()

    dean_df = assign_deans_subinstitution(dean_df, subinstitution_df)
    dean_df = process_matches(dean_df)
    dean_df = assign_remaining(dean_df, subinstitution_df)
    dean_df = assign_none(dean_df)
    dean_df = assign_administration(dean_df)
    dean_df = cleanup(dean_df)
    dean_df = expand_grouping(dean_df, subinstitution_df)
    dean_df = categorize_subinstitutions(dean_df)
    dean_df = clean_fixed_positions(dean_df)
    dean_df = add_seniority(dean_df)

    dean_df["Designation"] = dean_df["FixedPosition"]
    dean_df["FixedPosition"]  = "Dean"

    full_df.loc[dean_mask, ["FixedPosition", "Designation"]] = dean_df[["FixedPosition", "Designation"]]
    full_df.loc[dean_mask, "Seniority"] = dean_df["Seniority"]

    return full_df, dean_df

