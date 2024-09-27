import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.header('AIR CRASHES ANALYSIS FROM 1908 TO 2024')
st.subheader('AIR CRASHES DATA')
def datafile_load():
    data_file = 'aircrahesFullDataUpdated_2024.csv'
    df = pd.read_csv(data_file)
    # rename all columns in the dataset 
    df = df.rename({'Year': 'year', 
                'Quarter': 'quarter', 
                'Month': 'month', 
                'Day': 'day', 
                'Country/Region': 'country/region',
                'Aircraft Manufacturer':'aircraft manufacturer', 
                'Aircraft': 'aircraft', 
                'Location': 'location', 
                'Operator': 'operator', 
                'Ground': 'ground',
                'Fatalities (air)' :'fatalities (air)', 
                'Aboard' : 'aboard'},axis=1
              )
       
   # Replaces characters with values and empty string
    df['country/region'] = df['country/region'].str.replace('N/A', 'Other Places').str.replace('?', '').str.replace("'-",'Other Places')
    
    # Replace NaN with Other places
    df['country/region'] = df['country/region'].fillna('Other Places', inplace=False)

    # Replaces all characters with values and empty string as applicable
    df['aircraft manufacturer'] = df['aircraft manufacturer'].str.replace('N/A', 'Other manufacturer').str.replace('?', '').str.replace('+', '')
    
    # Replace NaN with Other manufacturer
    df['aircraft manufacturer'] = df['aircraft manufacturer'].fillna('Other manufacturer', inplace=False)

    # Replace N/A with Other Aircraft
    # Replace question mark with an empty string
    df['aircraft'] = df['aircraft'].str.replace('N/A', 'Other Aircraft').str.replace('?', '')

    # Replace NaN with Other Aircraft
    df['aircraft'] = df['aircraft'].fillna('Other Aircraft', inplace=False)

    # Replace question mark with an empty string
    df['location'] = df['location'].str.replace('?', '')

    # Replace NaN with Others
    df['location'] = df['location'].fillna('Others', inplace=False)

    # To avoid comma on the year column, convert it so string
    df['year'] = df['year'].astype(str) 

    # Replace question mark with an empty string * Replace N/A with 'Other operator'
    # Trim white spaces
    df['operator'] = df['operator'].str.replace('?', '').str.replace('N/A', 'Other operator').str.strip()

    # Replace NaN with Other operator
    df['operator'] = df['operator'].fillna('Other operator', inplace=False)

    
    return df
df = datafile_load()

st.dataframe(df)

# select and display specific Aircraft Manufacturer
# add a filter 
Aircraft_Manufacturer = df['aircraft manufacturer'].unique()
select_aircraft = st.sidebar.multiselect(
                    'Filter by Aircraft Manufacturer',
                    Aircraft_Manufacturer)
filtered_table = df[df['aircraft manufacturer'].isin(Aircraft_Manufacturer)]

st.subheader('METRICS')
# Variables for metrics
if len(filtered_table) > 0:
    Avg_ground_fatalities = filtered_table['ground'].mean()
else:
    Avg_ground_fatalities = df['ground'].mean()
if len(filtered_table) > 0:
    Avg_air_fatalities = filtered_table['fatalities (air)'].mean()
else: 
    Avg_air_fatalities = df['fatalities (air)'].mean()
if len(filtered_table) > 0:
    Avg_no_aboard = filtered_table['aboard'].mean()
else:
     Avg_no_aboard = df['aboard'].mean()

# Create the set of metrics (Average Values)
colA, colB, colC = st.columns(3)

colA.metric('Average Ground Fatalities',Avg_ground_fatalities)
colB.metric('Average Air Fatalities',Avg_air_fatalities)
colC.metric('Average Number Aboard',Avg_no_aboard)
# End of metrics

# add a filter table to the app
st.subheader('FILTERED TABLE')
st.dataframe(filtered_table[['year', 'quarter', 'month',
                            'aircraft manufacturer', 
                            'aircraft','operator', 'ground',
                            'fatalities (air)', 'aboard']])

# Add charts visualization to the app

st.subheader('VISUALIZATIONS')

# Trend in the number of aircraft crashes over the years
try:
    st.write('Trend in the Number of Aircraft Crashes over the Years')
    if len(filtered_table) > 0:
        crashes_per_year = filtered_table.groupby('year')['fatalities (air)'].count()
    else:
        crashes_per_year = df.groupby('year')['fatalities (air)'].count()
    
    crashes_per_year_df = crashes_per_year.reset_index()

    st.line_chart(crashes_per_year_df,
                  x='year', 
                  y = 'fatalities (air)')
except ValueError as v:
    st.error(
        """Error""" % v.reason
    )

# fatalities vary across different aircraft manufacturers
try:
    st.write('Analysis of Fatalities Across Different Aircraft Manufacturers')
    if len(filtered_table) > 0:
        fatalities_per_manufacturer = filtered_table.groupby('aircraft manufacturer')['fatalities (air)'].count().reset_index()
    else: 
        fatalities_per_manufacturer = df.groupby('aircraft manufacturer')['fatalities (air)'].count().reset_index()
    
    fatalities_per_manufacturer_df = fatalities_per_manufacturer.reset_index()

    st.line_chart(fatalities_per_manufacturer_df,
                 x='aircraft manufacturer', 
                 y = 'fatalities (air)')
except ValueError as v:
    st.error(
        """Error""" % v.reason
    )

