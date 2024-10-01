import streamlit as st

# Set page configuration
st.set_page_config(page_title="RAASMAN- SuperSite Home", layout="wide")

st.markdown("""
<style>
    body {
        background-color: #f5f5dc;  /* A mix of white and cream */
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
        background-color: #ffffff;  /* White background for sections */
    }
</style>
""", unsafe_allow_html=True)

# Homepage content
st.markdown("<h1 class='header'>Welcome to RAASMAN -  Supersite Dashboard </h1>", unsafe_allow_html=True)


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

