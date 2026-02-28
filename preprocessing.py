'''Analysis of Energy Inefficiency in Chicago
James Harren
Pre-Processing'''

# Imports
import pandas as pd
import numpy as np
import altair as alt
alt.data_transformers.disable_max_rows()
alt.renderers.enable("default")
import warnings
warnings.filterwarnings('ignore')


energy_use = pd.read_csv('data/external/Energy_Usage_2010.csv')

# RESIDENTIAL PROPERTIES
energy_use = energy_use[energy_use["BUILDING TYPE"]=='Residential']

# KWH PER SQFT
energy_use['TOTAL KWH'] = energy_use['TOTAL KWH'].str.replace(',', '').astype(float)
energy_use['KWH TOTAL SQFT'] = energy_use['KWH TOTAL SQFT'].str.replace(',', '').astype(float)
energy_use['KWH PER SQFT'] = energy_use['TOTAL KWH']/energy_use['KWH TOTAL SQFT']

# THERMS PER SQFT
energy_use['TOTAL THERMS'] = energy_use['TOTAL THERMS'].str.replace(',', '').astype(float)
energy_use['THERMS TOTAL SQFT'] = energy_use['THERMS TOTAL SQFT'].str.replace(',', '').astype(float)
energy_use['THERMS PER SQFT'] = energy_use['TOTAL THERMS']/energy_use['THERMS TOTAL SQFT']

# SEASONALITY CHECK
'''cols = list(energy_use.columns)
kwh_list = []
for mo in range(4, 16):
    kwh_mo = energy_use[cols[mo]].str.replace(',', '').astype(float)
    series = kwh_mo/energy_use['KWH TOTAL SQFT']
    average = series.mean()
    kwh_list.append(average)

therms_list = []
for mo in range(19, 31):
    therm_mo = energy_use[cols[mo]].str.replace(',', '').astype(float)
    series = therm_mo/energy_use['THERMS TOTAL SQFT']
    average = series.mean()
    therms_list.append(average)

months_avgs = pd.DataFrame({
    'Month': ['jan', 'feb', 'mar', 'april','may',
              'june','july','aug', 'sept', 'oct','nov','dec'],
    'KWH': kwh_list,
    'THERMS': therms_list,
})'''
# OUTCOME
# Found that highest KWH per SQFT is in July, lowest in April
# Found that highest THERMS per SQFT is in January, lowest in August

energy_use["THERM SPREAD"] = (energy_use['THERM JANUARY 2010'].str.replace(',', '').astype(float) - energy_use[
                                    'THERM AUGUST 2010'].str.replace(',', '').astype(float))/energy_use['THERMS TOTAL SQFT']
energy_use["KWH SPREAD"] = (energy_use['KWH JULY 2010'].str.replace(',', '').astype(float) - energy_use[
                                    'KWH APRIL 2010'].str.replace(',', '').astype(float))/energy_use['KWH TOTAL SQFT']

"""Energy Efficiency Measures Are:
THERM SPREAD - THIS IS MORE IMPORTANT/RELEVANT
KWH SPREAD
THERMS PER SQFT
KWH PER SQFT - THIS IS MORE IMPORTANT/RELEVANT"""

# AGGREGATE MEASURES BETWEEN RESIDENTIAL HOUSE TYPES TO BLOCKWIDE
# Only occupied properties
energy_use['OCCUPIED HOUSING UNITS'] = energy_use['OCCUPIED HOUSING UNITS'].str.replace(',', '').astype(float)
energy_use['OCCUPIED HOUSING UNITS'] = energy_use['OCCUPIED HOUSING UNITS'].fillna(0)
energy_use = energy_use[~(energy_use['OCCUPIED HOUSING UNITS']==0)]

def therm_weighted(x):
    return np.average(x, weights=energy_use.loc[x.index, 'THERMS TOTAL SQFT'])
def kwh_weighted(x):
    return np.average(x, weights=energy_use.loc[x.index, 'KWH TOTAL SQFT'])

energy_use['TOTAL POPULATION'] = energy_use['TOTAL POPULATION'].str.replace(',', '').astype(float)

energy_use_cb = energy_use.groupby('CENSUS BLOCK').agg(
    THERM_SPREAD=('THERM SPREAD', therm_weighted),
    THERMS_PER_SQFT = ('THERMS PER SQFT', therm_weighted),
    THERMS_BUILDING_AGE = ('AVERAGE BUILDING AGE', therm_weighted),
    KWH_SPREAD = ('KWH SPREAD', kwh_weighted),
    KWH_PER_SQFT = ('KWH PER SQFT', kwh_weighted),
    KWH_BUILDING_AGE = ('AVERAGE BUILDING AGE', kwh_weighted),
    PCT_RENT = ('RENTER-OCCUPIED HOUSING PERCENTAGE', np.mean),
    POPULATION = ('TOTAL POPULATION', np.mean),
    THERMS_SQFT = ('THERMS TOTAL SQFT', np.sum),
    KWH_SQFT = ('KWH TOTAL SQFT', np.sum)
)

energy_use_cb.reset_index(inplace=True)

# Add back community areas
comm_areas = energy_use[['COMMUNITY AREA NAME', 'CENSUS BLOCK']]
comm_areas = comm_areas.drop_duplicates(subset=['CENSUS BLOCK'])
energy_use_cb = pd.merge(energy_use_cb, comm_areas, 
                         on='CENSUS BLOCK', how='left')


# INCOME DATA FROM CENSUS
med_incs = pd.read_csv('data/external/2010_ACS_HH_Med_Inc_Cleaned.csv')

# EXTRACT CENSUS TRACT ID
med_incs['TRACT ID'] = med_incs['GEO_ID'].str[-6:]

energy_use_cb['CENSUS BLOCK'] = energy_use_cb['CENSUS BLOCK'].astype(int).astype(str)
energy_use_cb['TRACT ID'] = energy_use_cb['CENSUS BLOCK'].str[5:11]

# COMBINE
energy_use_cb = pd.merge(energy_use_cb, med_incs, on="TRACT ID", how='left')
energy_use_cb['Med_Inc_HH'] = energy_use_cb['Med_Inc_HH'].astype(int)

# AGGREGATE TO COMMUNITY AREA LEVEL

energy_use_cb = energy_use_cb.fillna(0)

def therm_weighted_cb(x):
    return np.average(x, weights=energy_use_cb.loc[x.index, 'THERMS_SQFT'])
def kwh_weighted_cb(x):
    return np.average(x, weights=energy_use_cb.loc[x.index, 'KWH_SQFT'])
def pop_weighted_cd(x):
    return np.average(x, weights=energy_use_cb.loc[x.index, 'POPULATION'])

energy_use_ca = energy_use_cb.groupby('COMMUNITY AREA NAME').agg(
    THERM_SPREAD=('THERM_SPREAD', therm_weighted_cb),
    THERMS_PER_SQFT = ('THERMS_PER_SQFT', therm_weighted_cb),
    THERMS_BUILDING_AGE = ('THERMS_BUILDING_AGE', therm_weighted_cb),
    KWH_SPREAD = ('KWH_SPREAD', kwh_weighted_cb),
    KWH_PER_SQFT = ('KWH_PER_SQFT', kwh_weighted_cb),
    KWH_BUILDING_AGE = ('KWH_BUILDING_AGE', kwh_weighted_cb),
    PCT_RENT = ('PCT_RENT', pop_weighted_cd),
    MED_INC = ('Med_Inc_HH', pop_weighted_cd),
    POPULATION = ('POPULATION', np.sum),
    THERMS_SQFT = ('THERMS_SQFT', np.sum),
    KWH_SQFT = ('KWH_SQFT', np.sum)
)

energy_use_ca = energy_use_ca.reset_index()

# ADD GEOGRAPHY
community = pd.read_csv('data/external/Chicago_CommunityAreas.csv')

community['COMMUNITY'] = community['COMMUNITY'].str.lower()
energy_use_ca['COMMUNITY AREA NAME'] = energy_use_ca['COMMUNITY AREA NAME'].str.lower()
community = community.rename(columns={'COMMUNITY': 'COMMUNITY AREA NAME'})

renaming = {
    'lakeview':'lake view',
    'o\'hare': 'ohare'
}
energy_use_ca['COMMUNITY AREA NAME'] = energy_use_ca['COMMUNITY AREA NAME'].replace(renaming)

energy_use_ca = pd.merge(energy_use_ca, community, on="COMMUNITY AREA NAME").rename(columns={'the_geom':'geometry'})

# CLEANING UP
energy_use_ca['Building_Age'] = (energy_use_ca['THERMS_BUILDING_AGE']+energy_use_ca['KWH_BUILDING_AGE'])/2
energy_use_ca = energy_use_ca[['COMMUNITY AREA NAME', 'THERM_SPREAD', 'THERMS_PER_SQFT',
        'KWH_SPREAD', 'KWH_PER_SQFT', 
       'PCT_RENT', 'MED_INC', 'Building_Age', 'POPULATION', 'THERMS_SQFT', 'KWH_SQFT',
       'geometry']]

renaming = {
    'lake view': 'lakeview',
    'ohare': 'o\'hare'
}

energy_use_ca['COMMUNITY AREA NAME'] = energy_use_ca['COMMUNITY AREA NAME'
                                                     ].replace(renaming).str.title()

# MAKE QUARTILES FOR HEATMAPPING

flip_map = {
    1: 5,
    2: 4,
    3: 3,
    4: 2,
    5: 1
}

energy_use_ca['RENTER_Q'] = pd.qcut(energy_use_ca['PCT_RENT'],q=5, labels=False)+1
energy_use_ca['HOMEOWNER_Q'] = energy_use_ca['RENTER_Q'].replace(flip_map)
energy_use_ca['OLD_BUILD_Q'] = pd.qcut(energy_use_ca['Building_Age'],q=5, labels=False)+1
energy_use_ca['NEW_BUILD_Q'] = energy_use_ca['OLD_BUILD_Q'].replace(flip_map)
energy_use_ca['HIGH_INC_Q'] = pd.qcut(energy_use_ca['MED_INC'],q=5, labels=False)+1
energy_use_ca['LOW_INC_Q'] = energy_use_ca['HIGH_INC_Q'].replace(flip_map)
energy_use_ca['HEAT_LEAK_Q'] = pd.qcut(energy_use_ca['THERM_SPREAD'],q=5, labels=False)+1
energy_use_ca['ENERGY_WASTE_Q'] = pd.qcut(energy_use_ca['KWH_PER_SQFT'],q=5, labels=False)+1

# OUTPUT TO CSV
energy_use_ca.to_csv('data/cleaned/Energy_Use_ComArea.csv')