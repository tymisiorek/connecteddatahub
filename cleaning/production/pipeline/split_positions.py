import pandas as pd
from pathlib import Path
from typing import List, Optional
import os

POSITION_BANK = [
    "President", "Chancellor", "Provost", "Director", "Dean", "Controller",
    "Trustee", "Member", "Regent", "Chairman", "Overseer", "Assistant",
    "Librarian", "Secretary", "Chaplain", "Minister", "Treasurer",
    "Senior Counsel", "General Counsel", "Legal Counsel", "University Counsel",
    "College Counsel", "Special Counsel", "Corporation Counsel",
    "Corporate Counsel", "Officer", "Chief", "Professor", "Commissioner",
    "Fellow", "Chairperson", "Manager", "Clergy", "Coordinator", "Auditor",
    "Governor", "Representative", "Stockbroker", "Advisor", "Commandant",
    "Rector", "Attorney", "Curator", "Clerk", "Department Head", "Pastor",
    "Head", "Comptroller", "Deputy", "Inspector General", "Instructor",
    "Registrar", "Ombuds", "Administrator", "Liaison",
    "Administrative Associate", "Webmaster", "Specialist",
    "University Planner", "Architect",
]

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
