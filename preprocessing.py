'''Analysis of Energy Inefficiency in Chicago
James Harren
Pre-Processing'''

# Imports
import pandas as pd

med_incs = pd.read_csv('data/external/2010_ACS_HH_Med_Inc_Cleaned.csv')

energy_use = pd.read_csv('data/external/Energy_Usage_2010.csv')

energy_use[energy_use['BUILDING TYPE']=='Residential']["CENSUS BLOCK"].iloc[4565]

energy_use[(energy_use['BUILDING TYPE']=='Residential') & 
                (energy_use['CENSUS BLOCK']==170312512003008)]



'''Get the income data over'''
# Need last 6 from the census to get tracts
med_incs

# Need to remove first five and get the next 6 digits.
energy_use.dtypes