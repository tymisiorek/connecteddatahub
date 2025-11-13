import pandas as pd
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
