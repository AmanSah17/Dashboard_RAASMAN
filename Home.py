import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(page_title="RAASMAN- SuperSite Home", layout="wide")

# Set up custom styling
st.markdown("""
<style>
    body {
        background-color: #f5f5dc;  /* Creamy background */
    }
    .header {
        font-size: 2em;
        text-align: center;
        margin: 20px 0;
        color: #4B0082;  /* Dark Violet */
    }
    .subheader {
        font-size: 1.5em;
        text-align: left;
        color: #333;  /* Dark Grey */
    }
    .content {
        font-size: 1em;
        text-align: justify;
        color: #444;  /* Medium Grey */
    }
    .section {
        border: 2px solid #4B0082;  /* Dark Violet */
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        background-color: #ffffff;  /* White background */
    }
</style>
""", unsafe_allow_html=True)

# Homepage content
st.markdown("<h1 class='header'>Welcome to RAASMAN - Supersite Dashboard</h1>", unsafe_allow_html=True)

# About RAASMAN section
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.markdown("<h2 class='subheader'>About RAASMAN</h2>", unsafe_allow_html=True)
st.markdown("""
<div class='content'>
    The website provides real-time data on the sources of air pollution in the city and is expected to help the Delhi government frame effective policies to curb it. 
    The website reflects data collected and processed by two laboratories — a ‘super site’ and a mobile laboratory. 
    The laboratories were used for the “real-time source apportionment study”, under which data on Delhi’s air were collected over many months, and a model (software) created, which shows the sources of air pollution by using air from the surroundings as input.
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    df = pd.read_csv('grouped_output.csv')
    df['Time (hour)'] = pd.to_datetime(df['Time (hour)'])
    df['Date'] = df['Time (hour)'].dt.date
    df['Hour'] = df['Time (hour)'].dt.hour
    return df

df = load_data()

# Streamlit app layout
st.title("Air Quality Dashboard")

# Date Picker
selected_date = st.date_input("Select Date", min_value=min(df['Date']), max_value=max(df['Date']))

# Filter data based on the selected date
date_filtered_df = df[df['Date'] == selected_date]

# Show hourly concentrations using Altair
if not date_filtered_df.empty:
    st.subheader(f"Hourly Pollutant Concentrations for {selected_date}")

    # Reshape data to make it compatible with Altair (melt the dataframe)
    hourly_data = date_filtered_df.melt(id_vars=['Time (hour)', 'Hour'], 
                                        value_vars=['CO', 'NO2', 'Ozone', 'SO2'], 
                                        var_name='Pollutant', 
                                        value_name='Concentration')

    # Create an Altair chart for hourly concentrations
    line_chart = alt.Chart(hourly_data).mark_line(point=True).encode(
        x=alt.X('Hour:O', title='Hour of Day (24-hour format)'),
        y=alt.Y('Concentration:Q', title='Concentration (µg/m³)'),
        color='Pollutant:N'
    ).properties(width=700, height=400, title=f"Hourly Pollutant Concentrations for {selected_date}")
    
    st.altair_chart(line_chart)

else:
    st.write("No data available for the selected date.")

# Time Selector (24-hour format)
selected_time = st.selectbox("Select Time (24-hour format)", [f"{i}:00" for i in range(24)])

# Convert the selected time into hour
selected_hour = int(selected_time.split(":")[0])

# Filter data based on selected date and time
filtered_df = df[(df['Date'] == selected_date) & (df['Hour'] == selected_hour)]

# Split view for bar chart and speedometers
if not filtered_df.empty:
    st.subheader(f"Concentrations for {selected_date} at {selected_time}")
    
    col1, col2 = st.columns(2)

    # Left column: Bar plot of pollutants concentrations
    with col1:
        st.write("### Pollutant Concentrations")

        # Reshape filtered data for Altair
        bar_data = filtered_df.melt(id_vars=['Time (hour)', 'Hour'], 
                                    value_vars=['CO', 'NO2', 'Ozone', 'SO2'], 
                                    var_name='Pollutant', 
                                    value_name='Concentration')

        # Create an Altair bar chart
        bar_chart = alt.Chart(bar_data).mark_bar().encode(
            x=alt.X('Pollutant:N', title='Pollutant'),
            y=alt.Y('Concentration:Q', title='Concentration (µg/m³)', scale=alt.Scale(domain=[0, 200])),
            color='Pollutant:N'
        ).properties(width=300, height=300, title=f"Pollutant Concentrations at {selected_time}")

        st.altair_chart(bar_chart)

    # Right column: Speedometer gauges for each pollutant
    with col2:
        st.write("### Pollutant Concentrations")
        
        # Create speedometer gauges for each pollutant
        fig = make_subplots(rows=2, cols=2, specs=[[{'type': 'indicator'}, {'type': 'indicator'}],
                                                   [{'type': 'indicator'}, {'type': 'indicator'}]])

        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=filtered_df['CO'].values[0],
            title={'text': "CO"},
            gauge={'axis': {'range': [None, 10]}}), row=1, col=1)

        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=filtered_df['NO2'].values[0],
            title={'text': "NO2"},
            gauge={'axis': {'range': [None, 100]}}), row=1, col=2)

        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=filtered_df['Ozone'].values[0],
            title={'text': "Ozone"},
            gauge={'axis': {'range': [None, 200]}}), row=2, col=1)

        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=filtered_df['SO2'].values[0],
            title={'text': "SO2"},
            gauge={'axis': {'range': [None, 20]}}), row=2, col=2)

        fig.update_layout(height=400, width=400, title_text="Pollutant Concentrations - Speedometer Gauges")
        st.plotly_chart(fig)

else:
    st.write("No data available for the selected time.")

# Interactive pollutant selection
if not date_filtered_df.empty:
    st.subheader(f"Available Pollutants for {selected_date}")

    # Pollutant selection buttons
    if st.button("CO"):
        co_data = date_filtered_df[['Hour', 'CO']].copy()
        max_co = co_data['CO'].max()
        co_chart = alt.Chart(co_data).mark_bar().encode(
            x=alt.X('Hour:O', title='Hour of Day (24-hour format)'),
            y=alt.Y('CO:Q', title='Concentration (µg/m³)', scale=alt.Scale(domain=[0, max_co + 1])),
            color=alt.value('blue')
        ).properties(width=700, height=300, title="Hourly CO Concentrations")
        st.altair_chart(co_chart)

    if st.button("NO2"):
        no2_data = date_filtered_df[['Hour', 'NO2']].copy()
        max_no2 = no2_data['NO2'].max()
        no2_chart = alt.Chart(no2_data).mark_bar().encode(
            x=alt.X('Hour:O', title='Hour of Day (24-hour format)'),
            y=alt.Y('NO2:Q', title='Concentration (µg/m³)', scale=alt.Scale(domain=[0, max_no2 + 5])),
            color=alt.value('orange')
        ).properties(width=700, height=300, title="Hourly NO2 Concentrations")
        st.altair_chart(no2_chart)

    if st.button("Ozone"):
        ozone_data = date_filtered_df[['Hour', 'Ozone']].copy()
        max_ozone = ozone_data['Ozone'].max()
        ozone_chart = alt.Chart(ozone_data).mark_bar().encode(
            x=alt.X('Hour:O', title='Hour of Day (24-hour format)'),
            y=alt.Y('Ozone:Q', title='Concentration (µg/m³)', scale=alt.Scale(domain=[0, max_ozone + 5])),
            color=alt.value('green')
        ).properties(width=700, height=300, title="Hourly Ozone Concentrations")
        st.altair_chart(ozone_chart)

    if st.button("SO2"):
        so2_data = date_filtered_df[['Hour', 'SO2']].copy()
        max_so2 = so2_data['SO2'].max()
        so2_chart = alt.Chart(so2_data).mark_bar().encode(
            x=alt.X('Hour:O', title='Hour of Day (24-hour format)'),
            y=alt.Y('SO2:Q', title='Concentration (µg/m³)', scale=alt.Scale(domain=[0, max_so2 + 2])),
            color=alt.value('purple')
        ).properties(width=700, height=300, title="Hourly SO2 Concentrations")
        st.altair_chart(so2_chart)
else:
    st.write("No data available for the selected date.")
