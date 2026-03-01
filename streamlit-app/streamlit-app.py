# Streamlit Dashboard for Final Project

import streamlit as st
import os

BASE_DIR = os.path.dirname(__file__)

st.set_page_config(page_title="Chicago Energy Efficiency Policy Tuner")

# DATA LINKS

def intro():
    import streamlit as st
    st.write("# Chicago Energy Efficiency Policy Tuner")
    st.markdown(
    '''
    Chicago aims to increase energy efficiency of the city's building stock as a climate change initiative. Some grants are available through the Green Homes Chicago program to support energy efficiency upgrades, however, future programs may want to be more focused.  

    Energy efficiency programs can focus on improving building insulation or upgrading wasteful applicances.
    
    In order to more effectively target buildings that need upgrades, energy use data from 2010 for the city is analyzed to understand what kind of people or buildings tend to be more wasteful.
    
    First Chicago can make their energy efficiency grants more specific in what they will fund. Potential policies are:
    - **Weatherization Policy**, funding insulation or window improvements in the city. This option is analyzed through examining the difference between the highest month's average gas use, January, and the lowest month's average gas use, August, and dividing by the square footage of the building. 
    - **Appliance Upgrade Policy**, funding new more efficient appliances. This option is analyzed through examining yearly KWHs per square foot.

    Aside from the policy design, energy efficiency grantmaking or other policies usually target specific audiences. The following characteristics are analyzed on this page:
    - **Average Building Age**
    - **Median Household Income**
    - **Percent of Units Occupied by Renters**

    The Policy Construction page allows officials to see what characteristics correlate with higher energy use for each potential policy. Then, the Outreach Priority Map page allows officials to understand what Community Areas in Chicago should be the focus of outreach. 
    '''
    )

def corr():
    import streamlit as st
    import pandas as pd
    import os 
    import altair as alt

    st.write("## Policy Construction")
    st.write("#### Checkout what kind of policy and characterization to prioritize:")
    col1, col2 = st.columns(2)
    with col1:
        policy = st.radio(
        "Which Policy Focus?",
        key="policy",
        options=["Weatherization", "Appliance Upgrade"]
        )
    with col2:
        character = st.radio(
        "Which Characterization?",
        key="character",
        options=["Building Age", "Income", "Renter Status"]
        )
    
    df = pd.read_csv(os.path.join(BASE_DIR, "Energy_Use_ComArea.csv"))
    axis_dict = {
        'Weatherization':'Seasonal Difference in Gas Use',
        'Appliance Upgrade':'Electricity Use per SQFT'
    }
    policy_dict = {
        'Weatherization':'THERM_SPREAD',
        'Appliance Upgrade':'KWH_PER_SQFT'
    }
    character_dict = {
        'Building Age':'Building_Age',
        'Income':'MED_INC',
        'Renter Status':'PCT_RENT'
    }
    chart = alt.Chart(df,
                title = alt.TitleParams(text = f"Relationship between {axis_dict[policy]} and {character}")
                ).mark_circle().encode(
                alt.X(character_dict[character], 
                      title=character),
                alt.Y(policy_dict[policy], 
                      title=axis_dict[policy]))

    line = chart.transform_regression(
                        character_dict[character], 
                        policy_dict[policy]).mark_line(color="grey")

    final = chart + line
    st.altair_chart(final)

def mapper():
    import streamlit as st
    import pandas as pd
    import geopandas as gpd
    from shapely import wkt
    import plotly.express as px
    import json

    st.write("## Outreach Priority Map")
    st.write("#### Checkout what kind of policy and characterization to prioritize:")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        policy = st.radio(
        "Which Policy Focus?",
        key="policy",
        options=["Weatherization", "Appliance Upgrade"]
        )
    with col2:
        building = st.radio(
        "Prioritize by Building Age?",
        key="building",
        options=["Old Buildings", "New Buildings", "Neither"]
        )
    with col3:
        income = st.radio(
        "Prioritize by Income?",
        key="income",
        options=["Low Income", "High Income", "Neither"]
        )
    with col4:
        renter = st.radio(
        "Prioritize by Renter Status?",
        key="renter",
        options=["Renters", "Homeowners", "Neither"]
        )

    data = pd.read_csv(os.path.join(BASE_DIR, "Energy_Use_ComArea.csv"))
    data['geometry'] = data['geometry'].apply(wkt.loads)
    city = gpd.GeoDataFrame(data, geometry='geometry', crs='EPSG:4326')
    

    policy_dict = {
        'Weatherization':'HEAT_LEAK_Q',
        'Appliance Upgrade':'ENERGY_WASTE_Q'
    }
    build_dict = {
        'Old Buildings':'OLD_BUILD_Q',
        'New Buildings':'NEW_BUILD_Q',
        'Neither':'Neither'
    }
    inc_dict = {
        'Low Income':'LOW_INC_Q',
        'High Income':'HIGH_INC_Q',
        'Neither':'Neither'
    }
    renter_dict = {
        'Renters':'RENTER_Q',
        'Homeowners':'HOMEOWNER_Q',
        'Neither':'Neither'
    }
    city['Neither'] = 0
    city['Priority'] = city[policy_dict[policy]
                             ] +city[build_dict[building]
                            ] + city[inc_dict[income]
                            ] +city[renter_dict[renter]]
    
    city = city.reset_index().rename(columns={"index": "id"})
    city_json = json.loads(city.to_json())

    fig = px.choropleth(
        city,
        geojson=city_json,
        locations='id',
        featureidkey="properties.id", 
        color='Priority',    
        hover_name='COMMUNITY AREA NAME',
        hover_data = {'PCT_RENT':':.2%', 'MED_INC':':.0f', "Building_Age":':.2f', 'id':False,'Priority':False},   
        color_continuous_scale="OrRd",
        fitbounds='geojson')
    fig.update_geos(visible=False)
    st.plotly_chart(fig, width=True)
    

page_names_to_funcs = {
    "Welcome!": intro,
    "Policy Construction": corr,
    "Outreach Priority Map": mapper
}
page_name = st.sidebar.selectbox("Choose a step", page_names_to_funcs.keys())
page_names_to_funcs[page_name]()