# Chicago Energy Inefficiency Analysis

This project analyzes what kinds of neighborhoods have the worst energy efficiency and what neighborhoods are most likely to benefit from different energy efficiency policies.  

## Setup

Make sure the correct environment is set up. Run the following in terminal:

```bash
conda env create -f environment.yml
conda activate chi_energy_eff
```

## Project Structure

```
data/
	external/           		# Raw data files
    		Energy_Usage_2010.csv 		# Chicago Energy Use
		Chicago_CommunityAreas.csv 		# Chicago Community Areas
		ACS_Data.csv					# Raw U.S. Census Data
  	cleaned/            	# Initial cleanup of Census Data
    		ACS_Data_Clean.csv			# Cleaned U.S. Census Data processed with preprocessing.py
code/
  	preprocessing.py    # Removes non-data row and subsets and renames columns in Raw U.S. Census Data
streamlit-app/
	streamlit-app.py			# Python file needed to run streamlit in community cloud
	Energy_Use_ComArea.csv		# Data needed to run streamlit app
	requirements.txt			# Pip dependencies for the streamlit app
```

## Streamlit App

[Checkout this project's interactive dashboard!](https://dap-final-chicago-energy.streamlit.app/)

Please note that Streamlit Apps hosted on the community cloud, as this one is, must be 'woken up' when inactive for more than 24 hours, so its initial loading time may be longer than usual. 

## Data Sources

1. "Energy Usage 2010." *Chicago Data Portal*. Accessed March 4th, 2026, at https://data.cityofchicago.org/Environment-Sustainable-Development/Energy-Usage-2010/8yq3-m6wp/about_data

File saved as "Energy_Usage_2010.csv"

2. U.S. Census Bureau. "2006-2010 American Community Survey." Accessed March 4th, 2026, at https://data.census.gov/

Survey data S1903, "Median Income in the Past 12 Months" were downloaded for "All Census Tracts within Cook County" for "2010" using the U.S. Census Bureau's interactive data download site above. 

File saved as "ACS_Data.csv"

3. "Boundaries - Community Areas." *Chicago Data Portal* Accessed March 4th, 2026 at https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Community-Areas/igwz-8jzy/about_data

File saved as "Chicago_CommunityAreas.csv"

