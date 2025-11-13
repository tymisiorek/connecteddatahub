import os
import pandas as pd
from presidents import *
from provost import *
from boards import *
from vice_presidents import *
from deans import *
from split_positions import *


data_path = r"C:\Projects\connecteddatahub\data"
years = ["1999","2000","2005","2007","2008","2009","2010","2011","2013","2018",]
# years = ['1999']

combined = []
def full_pipeline(full_df, grouped_df):
    full_df, pres_df = process_presidents(full_df)
    full_df, prov_df = process_provost(full_df, grouped_df)
    full_df, vp_df = process_vice_presidents(full_df, grouped_df)
    full_df, board_df = process_boards(full_df)
    full_df, dean_df = process_deans(full_df, grouped_df)
    return full_df, pres_df, prov_df, board_df, vp_df, dean_df

#subinstitution translation dict
subinstitution_df = pd.read_csv(os.path.join(data_path, 'cleaned_dataframes', 'subinstitutions', 'validated_subinstitutions.csv'))

#state system mapping
map_df = pd.read_csv(os.path.join(data_path, 'maps', 'cleaned_affiliation.csv'))
map_df['Institution'] = map_df['FullName']
system_map = map_df.set_index('AffiliationId')['SystemId']

# build lowercase institution map for case‐insensitive lookup
inst_map_ci = {inst.lower(): sid for inst, sid in zip(map_df['Institution'], map_df['SystemId'])}


for year in years:
    print(f"On: {year}")
    df = pd.read_csv(os.path.join(data_path, 'backup', 'gpt_dataframes', f'cleaned_leadership{year}.csv'))

    #add state system mapping on
    aff_map = dict(zip(map_df['AffiliationId'], map_df['SystemId']))
    df['SystemId'] = df['AffiliationId'].map(aff_map)
    mask = df['SystemId'].isna()
    df.loc[mask, 'SystemId'] = (df.loc[mask, 'Institution'].str.lower().map(inst_map_ci))

    #mask out non sample or state systems
    df = df[(df['PrimarySample'] == True) | (df['SystemId'].notna())]
    df['FixedPosition'] = ""
    df['Seniority'] = ""
    df['Designation'] = ""

    #split rows into two if the position contains multiple positions
    df = apply_splitting_pipeline(df)
    
    df, pres_df, prov_df, board_df, vp_df, dean_df = full_pipeline(df, subinstitution_df)
    combined.append(df)
    df.to_csv(os.path.join(data_path, 'cleaned_dataframes', f'{year}_cleanedDataframe.csv'), index = False)
    # board_df.to_csv(os.path.join(data_path, 'boards', f'{year}_boards.csv'), index = False)
    # dean_df.to_csv(os.path.join(data_path, f'{year}_deans.csv'))
    # vp_df.to_csv(os.path.join(data_path, f'{year}_vps.csv'))
# combined_df = pd.concat(combined, ignore_index=True)