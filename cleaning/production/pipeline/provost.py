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

def mark_first_provost_positions(df):
    """Mark the first acceptable 'Provost' per institution, return a solely provost df and the original df with an updated 'FixedPosition' column"""
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

    generic_titles = {"Provost", "Executive Provost", "Head Provost", "Chief Provost",}
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

    df["Category"] = df.set_index(["Institution", "SubInstitution"]).index.map(subinstitution_dict)

    
    mask_a = (df["FixedPosition"].str.contains("SubInstitution|Other", na=False) & df["SubInstitution"].notna()& (df["provost_index"] == df["PositionTitle"].str.len()))
    df.loc[mask_a, "FixedPosition"] = df.loc[mask_a, "Category"].where(df.loc[mask_a, "Category"] != "Error", other="Generic")
    #run through keyword dictionary 
    mask_b = (df["FixedPosition"].str.contains("SubInstitution", na=False) & (df["provost_index"] != df["PositionTitle"].str.len()))
    df.loc[mask_b, "FixedPosition"] = df.loc[mask_b, "PositionTitle"].apply(lambda pos: assign_position_grouping_subinst(pos, "Provost,"))
    #misc classifcations
    mask_c = ((df["provost_index"] != df["PositionTitle"].str.len()) & df["SubInstitution"].isna() & df["FixedPosition"].str.contains("Other", na=False))
    def classify_or_other(pos):
        c = assign_position_grouping_subinst(pos, "Provost,")
        return c if c else "Other"
    df.loc[mask_c, "FixedPosition"] = df.loc[mask_c, "PositionTitle"].apply(classify_or_other)

    mask_other = df["FixedPosition"] == "Other"
    df.loc[mask_other, "FixedPosition"] = df.loc[mask_other, "PositionTitle"].apply(classify_or_other)

    return df.drop(columns=["PositionTitle", "provost_index", "Category"])

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

def last_sweep(df):
    out = df.copy()
    out['FixedPosition'] = out['FixedPosition'].fillna("").replace("", "Other")
    return out


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

    #set Designation and reset FixedPosition label
    provost_df['Designation'] = provost_df['FixedPosition']
    provost_df['FixedPosition'] = 'Provost'

    #prepend "Vice " to FixedPosition where Position contains "Vice"
    #prepend "Vice " only on those rows that actually have "Vice" in Position
    vm = provost_df['Position'].str.contains('Vice', case=False, na=False)
    provost_df.loc[vm, 'FixedPosition'] = ('Vice ' + provost_df.loc[vm, 'FixedPosition'])

    # overwrite with head provost rows 
    provost_df.loc[head_provost_df.index, ['FixedPosition', 'Designation']] = head_provost_df[['FixedPosition', 'Designation']]

    # if head_provost_df contains a Seniority column, bring it across
    full_df.loc[mask, 'Seniority'] = provost_df['Seniority']
    # write back into the full_df
    full_df.loc[mask, ['FixedPosition', 'Designation', 'Seniority']] = provost_df[['FixedPosition', 'Designation', 'Seniority']]
    return full_df, provost_df
