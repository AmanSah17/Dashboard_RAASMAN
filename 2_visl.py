import streamlit as st
import pandas as pd
import altair as alt

# Load the CSV file
df = pd.read_csv('grouped_output.csv')

# Convert 'Time (hour)' to datetime
df['Time (hour)'] = pd.to_datetime(df['Time (hour)'])
df['Date'] = df['Time (hour)'].dt.date
df['Hour'] = df['Time (hour)'].dt.hour

# Streamlit app layout
st.title("Air Quality Dashboard")

# Sidebar for navigation
st.sidebar.header("Navigation")
st.sidebar.markdown("[View Source Code](<URL_TO_YOUR_CODE>)")  # Replace <URL_TO_YOUR_CODE> with the actual link

# Date Picker
selected_date = st.date_input("Select Date", min_value=min(df['Date']), max_value=max(df['Date']))

# Filter data based on the selected date
date_filtered_df = df[df['Date'] == selected_date]

# Check if data is available for the selected date
if not date_filtered_df.empty:
    st.subheader(f"Available Pollutants for {selected_date}")

    # Create a row for CO
    co_button = st.button("CO")
    if co_button:
        co_data = date_filtered_df[['Hour', 'CO']].copy()
        max_co = co_data['CO'].max()
        co_chart = alt.Chart(co_data).mark_bar().encode(
            x=alt.X('Hour:O', title='Hour of Day (24-hour format)'),
            y=alt.Y('CO:Q', title='Concentration (µg/m³)', scale=alt.Scale(domain=[0, max_co + 10])),
            color=alt.value('blue')
        ).properties(width=700, height=300, title="Hourly CO Concentrations")
        st.altair_chart(co_chart)

    # Create a row for NO2
    no2_button = st.button("NO2")
    if no2_button:
        no2_data = date_filtered_df[['Hour', 'NO2']].copy()
        max_no2 = no2_data['NO2'].max()
        no2_chart = alt.Chart(no2_data).mark_bar().encode(
            x=alt.X('Hour:O', title='Hour of Day (24-hour format)'),
            y=alt.Y('NO2:Q', title='Concentration (µg/m³)', scale=alt.Scale(domain=[0, max_no2 + 10])),
            color=alt.value('orange')
        ).properties(width=700, height=300, title="Hourly NO2 Concentrations")
        st.altair_chart(no2_chart)

    # Create a row for Ozone
    ozone_button = st.button("Ozone")
    if ozone_button:
        ozone_data = date_filtered_df[['Hour', 'Ozone']].copy()
        max_ozone = ozone_data['Ozone'].max()
        ozone_chart = alt.Chart(ozone_data).mark_bar().encode(
            x=alt.X('Hour:O', title='Hour of Day (24-hour format)'),
            y=alt.Y('Ozone:Q', title='Concentration (µg/m³)', scale=alt.Scale(domain=[0, max_ozone + 10])),
            color=alt.value('green')
        ).properties(width=700, height=300, title="Hourly Ozone Concentrations")
        st.altair_chart(ozone_chart)

    # Create a row for SO2
    so2_button = st.button("SO2")
    if so2_button:
        so2_data = date_filtered_df[['Hour', 'SO2']].copy()
        max_so2 = so2_data['SO2'].max()
        so2_chart = alt.Chart(so2_data).mark_bar().encode(
            x=alt.X('Hour:O', title='Hour of Day (24-hour format)'),
            y=alt.Y('SO2:Q', title='Concentration (µg/m³)', scale=alt.Scale(domain=[0, max_so2 + 10])),
            color=alt.value('red')
        ).properties(width=700, height=300, title="Hourly SO2 Concentrations")
        st.altair_chart(so2_chart)

else:
    st.write("No data available for the selected date.")
