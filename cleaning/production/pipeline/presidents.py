import pandas as pd
from constants import *


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

def process_presidents(full_df):
    return mark_president_positions(full_df)