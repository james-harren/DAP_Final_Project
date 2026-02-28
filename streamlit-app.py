# Streamlit Dashboard for Final Project

import streamlit as st
import os

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
    - **Appliance Policy**, funding new more efficient appliances. This option is analyzed through examining yearly KWHs per square foot.

    Aside from the policy design, energy efficiency grantmaking or other policies usually target specific audiences. The following characteristics are analyzed on this page:
    - **Average Building Age**
    - **Median Household Income**
    - **Percent of Units Occupied by Renters**

    The Policy Construction page allows officials to see what characteristics correlate with higher energy use for each potential policy. Then, the Outreach Priority Map page allows officials to understand what Community Areas in Chicago should be the focus of outreach. 
    '''
    )

def corr():
    st.write('Page under construction')

def mapper():
    st.write('Page under construction')


page_names_to_funcs = {
    "Welcome!": intro,
    "Policy Construction": corr,
    "Outreach Priority Map": mapper
}
page_name = st.sidebar.selectbox("Choose a step", page_names_to_funcs.keys())
page_names_to_funcs[page_name]()