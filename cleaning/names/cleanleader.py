import os
import re
import pandas as pd
import numpy as np
import unicodedata

from scipy.sparse.csgraph import connected_components

from position_word_banks import *

def normalize_text(s):
    if isinstance(s, str):
        return unicodedata.normalize('NFKC', s)
    return s

def replace_elements(df, col_name, elements2replace = None):

    for abbr, full in elements2replace:
        df[col_name] = df[col_name].str.replace(re.compile(r'\b' + re.escape(abbr) + r'\b'), full, regex=True)

    return df

def empty_str_mode(a):
    
    values, counts = np.unique(a, return_counts=True)
    if values.shape[0] == 0:
        return ""
    else:
        return np.random.choice(values[counts==counts.max()],1)[0]


##############################
# Process Names
##############################
def identify_true_name(exp_affsub, candidate_idx):
    common_names = [empty_str_mode([n for n in exp_affsub.loc[candidate_idx, col].values if len(n)>0]) for col in ['LastName', 'NickName', 'SuffixName', 'PrefixName']]

    fname_opts = [n for n in exp_affsub.loc[candidate_idx, 'FirstName'].values if not n in exp_affsub.loc[candidate_idx, 'NickName'].values]
    common_fname = empty_str_mode(fname_opts)

    pmiddlenames = [m for m in exp_affsub.loc[candidate_idx, 'MiddleName'].values]
    longest_mid = max(pmiddlenames, key=len, default=None)

    most_initials = [m for m in exp_affsub.loc[candidate_idx, 'MiddleInitials'].values]
    most_mid_init = max(most_initials, key=len, default=None)

    return [common_fname, longest_mid, most_mid_init] + common_names

##############################
# Process Positions
##############################

# SPLIT Multiple Positions
def contains_position(text: str) -> bool:
    """Return True iff any word from POSITION_BANK appears in *text*."""
    return any(title in text for title in POSITION_BANK)

    
def count_appearances(text: str) -> int:
    """How many distinct bank titles appear (substring match)."""
    return sum(1 for title in POSITION_BANK if title in text)


def all_split_indices(text: str, sep: str) -> list[int]:
    """Return a list of all positions where `sep` occurs in `text`."""
    idxs = []
    start = 0
    while True:
        i = text.find(sep, start)
        if i < 0:
            return idxs
        idxs.append(i)
        start = i + len(sep)

def split_position_rows(df: pd.DataFrame) -> pd.DataFrame:
    new_rows = []
    for _, row in df.iterrows():
        pos = (str(row["Position"]) if not pd.isna(row["Position"]) else "").title()
        split_done = False

        for sep in ("And", ";", ","):
            # Try this delimiter up to three times
            for _ in range(3):
                for idx in reversed(all_split_indices(pos, sep)):
                    left  = pos[:idx].strip()
                    right = pos[idx + len(sep):].strip()

                    #never split if the LHS has no known title
                    if not contains_position(left):
                        continue

                    #skip unwanted “office of the” fragments e.g 'Director, Office of the Provost" would split into 2, but this is just one
                    low = right.lower()
                    if ("office of the" in low or "to the" in low or "'s office" in low or "for the" in low) and count_appearances(right) < 2:
                        continue

                    #if both sides now both contain a title, accept the split
                    if contains_position(right):
                        top = row.copy(); top["Position"] = left
                        bottom = row.copy(); bottom["Position"] = right
                        new_rows.extend((top, bottom))
                        split_done = True
                        break

                if split_done:
                    break
            if split_done:
                break
        if not split_done:
            new_rows.append(row)
    return pd.DataFrame(new_rows).reset_index(drop=True)

def apply_splitting_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    df = split_position_rows(df)
    df = split_position_rows(df)
    df = split_position_rows(df)
    return df


# FOCUS on presidents

def is_true_president(pos):
    pos = str(pos).lower()
    return any(p in pos for p in PRESIDENT_WORDS) and "vice" not in pos





##############################
# Process Names
##############################


def split_job_titles(title, position_pattern):
    ## OLD
    """
    Splits job titles into distinct positions while keeping roles within a single title.
    
    Example:
        - "Provost and Vice President" -> ["Provost", "Vice President"]
        - "Vice President, Students and Faculty" -> ["Vice President, Students and Faculty"]
    """

    # Tokenize the title
    #tokens = re.split(r'\s*,\s*|\s+and\s+|\s+or\s+|\s*&\s*', title)
    tokens = re.split(r'(\s+,\s+|\s+and\s+|\s+or\s+|\s+&\s+)', title) # includes the conjunctions
    split_titles = []
    current_title = []
    
    
    for token in tokens:
        if position_pattern.search(token) and current_title:
            # If we hit a new title and there is already a current title, finalize it
            
            split_titles.append(" ".join(current_title[:-1]).strip())
            current_title = [token]
        else:
            current_title.append(token)
    
    # Append the last collected title
    if current_title:
        split_titles.append(" ".join(current_title).strip())
    
    return split_titles