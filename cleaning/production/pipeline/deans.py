import pandas as pd
from constants import *
import re

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
    #assign deans according to their subinstitutions 
    deans_df["FixedPosition"] = ""

    subinst_cat = (subinstitution_df.set_index(["Institution", "SubInstitution"])["Category"].to_dict())
    #pre-compute helpers
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
    deans_df.loc[mask, "FixedPosition"] = (pd.Series(keys, index=deans_df.index[mask]).map(subinst_cat))

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

    #rows whose FixedPosition was originally blank
    mask_empty = df["FixedPosition"] == ""
    df.loc[mask_empty, 'FixedPosition'] = (pos_title[mask_empty].apply(lambda p: assign_position_grouping_subinst(p, 'Dean,')))

    #same blank rows where "Dean" ends the string
    mask_end = mask_empty & (dean_idx == pos_len)
    df.loc[mask_end, "FixedPosition"] = "Generic"

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
    cleanup_list = ["Faculty", "Administrator", "Students", "Administrative", "Enrollment", "Finance", "Foundation", "Student", "Academic Affair", "Programs", "Alumni", "Relations", "Conservatory", "Division", "Professions", "Practice", "Educational", "Office", "Management"]
    pattern = '|'.join(map(re.escape, cleanup_list))
    pos_title = deans_df['Position'].fillna('').astype(str).str.title()
    altered = pos_title.apply(remove_parentheses).str.strip()
    dean_idx = altered.str.rfind('Dean') + 4
    not_at_end = dean_idx != altered.str.len()

    sub_title = deans_df['SubInstitution'].fillna('').astype(str).str.title()

    # check if Position or SubInstitution contain a keyword
    pos_hit = pos_title.str.contains(pattern, na=False)
    sub_hit = sub_title.str.contains(pattern, na=False)

    #relabel such rows
    mask = (not_at_end & (pos_hit | sub_hit) & (deans_df['FixedPosition'] != 'Administration'))

    deans_df.loc[mask, 'FixedPosition'] = 'Administration'
    return deans_df
        

def expand_grouping(deans_df, subinstitution_df):
    #add onto the existing classifcations
    df = deans_df.copy()
    subinst_cat = subinstitution_df.set_index(['Institution', 'SubInstitution'])['Category'].to_dict()

    sub_title = df['SubInstitution'].fillna("").astype(str).str.title()
    pos_title = df['Position'].fillna("").astype(str).str.title()

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

    mask_lib = pos_title.str.contains('Librar', na=False) & ~key_str.str.contains('Information', case=False, na=False)
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


def process_deans(full_df, subinstitution_df):
    """
    Extract and classify all Dean rows, update full_df, and return both full_df and dean_df.
    """
    dean_mask = (full_df["Position"].str.contains(r"\bDean\b", case=False, na=False) & ~full_df["Position"].str.contains(r"Assistant to the Dean", case=False, na=False))
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
