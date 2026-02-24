# Chicago Energy Inefficiency Analysis

This project analyzes where energy inefficient buildings are in the city, and 

## Setup

```bash
conda env create -f environment.yml
conda activate chi_energy_eff
```

## Project Structure

```
data/
  raw-data/           # Raw data files
    WHAT ARE
  derived-data/       # Filtered data and output plots
    WHAT ARE
code/
  preprocessing.py    # What does it do?
```

## Usage

1. Run preprocessing to filter data:
   ```bash
   python code/preprocessing.py
   ```

2. Generate the fire perimeter plot:
   ```bash
   python code/plot_fires.py
   ```
   
## Streamlit App

LINK

## Data Sources

1. Chicago Energy Usage 2010 database. https://data.cityofchicago.org/Environment-Sustainable-Development/Energy-Usage-2010/8yq3-m6wp/about_data 

2. Census data (U.S. Census Bureau, 2006-2010 American Community Survey) 
- Downloaded from... https://data.census.gov/ filtering for Cook County + Census Tracts + Income and Poverty and then downloading for S1903 "Median Income in the Past 12 Months"
 
- Cleaned to remove extraneous columns to only include the following:
GEO_ID	
NAME	
S1903_C01_001E	RENAMED TO Num_HH (i.e. Number of Households)
S1903_C02_001E	RENAMED TO Med_Inc_HH (i.e. Median Household Income)

- Community Areas https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Community-Areas/igwz-8jzy/about_data
- Census blocks https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Census-Blocks-2010/mfzt-js4n 

