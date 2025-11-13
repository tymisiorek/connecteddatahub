from position_disambiguate import *
import pandas as pd
import os

data_path = r"C:\Projects\connecteddatahub\data\cleaned_dataframes"
# years = [1999, 2000, 2002, 2005, 2007, 2008, 2009, 2010, 2011, 2013, 2018]
years = ["1999", "2000", "2002", "2005", "2007", "2008", "2009", "2010", "2011", "2013", "2018"]

combined = []
def full_pipeline(full_df, grouped_df):
    full_df, pres_df = process_presidents(full_df)
    full_df, prov_df = process_provost(full_df, grouped_df)
    full_df, vp_df = process_vice_presidents(full_df, grouped_df)
    full_df, board_df = process_boards(full_df)
    full_df, dean_df = process_deans(full_df, grouped_df)
    return full_df, pres_df, prov_df, board_df, vp_df, dean_df


subinstitution_df = pd.read_csv(os.path.join(data_path, 'subinstitutions', 'validated_subinstitutions.csv'))
for year in years:
    df = pd.read_csv(os.path.join(data_path, 'split_positions', f'{year}_split_positions.csv'))
    #mask out non sample or state systems
    df = df[(df['PrimarySample'] == True) | (df['SystemId'].notna())]
    df['FixedPosition'] = ""
    df['Seniority'] = ""
    df['Designation'] = ""
    
    df, pres_df, prov_df, board_df, vp_df, dean_df = full_pipeline(df, subinstitution_df)
    combined.append(df)
    df.to_csv(os.path.join(data_path, f'{year}_cleanedDataframe.csv'), index = False)
    board_df.to_csv(os.path.join(data_path, 'boards', f'{year}_boards.csv'), index = False)
    dean_df.to_csv(os.path.join(data_path, "deans", f'{year}_deans.csv'))
    vp_df.to_csv(os.path.join(data_path, "vps", f'{year}_vps.csv'))
    pres_df.to_csv(os.path.join(data_path, "presidents", f'{year}_presidents.csv'))
    prov_df.to_csv(os.path.join(data_path, "provost", f'{year}_provost.csv'))
# combined_df = pd.concat(combined, ignore_index=True)