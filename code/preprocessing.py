"James Harren"
"Preprocessing of ACS file"

import pandas as pd

census_data = pd.read_csv('../data/external/ACS_Data.csv')
census_data = census_data.drop(0)
columns = ['GEO_ID', 'NAME','S1903_C01_001E', 'S1903_C02_001E']
census_data = census_data[columns]
census_data = census_data.rename(columns={'S1903_C01_001E':'Num_HH', 'S1903_C02_001E':'Med_Inc_HH'})
census_data = census_data.reset_index().drop('index', axis=1)
census_data.to_csv('../data/cleaned/ACS_Data_Clean.csv')