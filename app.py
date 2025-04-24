import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

st.set_page_config(page_title="College Cutoff Filter", layout="wide")
st.title("College Cutoff Rank Filter (JEE MAINS AND JEE ADVANCED)")

# Form input
with st.form("cutoff_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        exam = st.selectbox("Select Exam", ["JEE MAIN", "JEE ADVANCED"])
    with col2:
        category = st.selectbox("Select Category", ["OPEN", "EWS", "OBC-NCL", "SC", "ST"])
    with col3:
        gender = st.selectbox("Select Gender", ["Gender-Neutral", "Female"])

    lower = st.number_input("Lower Rank Limit", min_value=0, value=0)
    upper = st.number_input("Upper Rank Limit", min_value=0, value=100000)
    submitted = st.form_submit_button("Filter")

# Placeholder for filtered results
result_df = pd.DataFrame()

if submitted:
    st.write(f"### Results for {category} - {gender} between ranks {lower} and {upper} , ROUND 5 2024")
    
    if exam == "JEE MAIN":
        data = pd.read_csv("jossa R5 cutoffCSV.csv")
        new_data = data[data["Seat Type"] == category]
        filtered_data = new_data[(new_data["Closing Rank"] > lower) & (new_data["Closing Rank"] < upper)]

        if gender == "Female":
            gender = "Female-only (including Supernumerary)"

        hs_data = filtered_data[(filtered_data["Quota"] == "HS") & (filtered_data["Gender"] == gender)]
        os_data = filtered_data[(filtered_data["Quota"] == "OS") & (filtered_data["Gender"] == gender)]

        hs_data = hs_data.sort_values("Closing Rank")
        os_data = os_data.sort_values("Closing Rank")
        combined_data = pd.concat([os_data, hs_data], ignore_index=True)
        combined_data.reset_index(drop=True, inplace=True)
        combined_data.index += 1
        result_df = combined_data

    elif exam == "JEE ADVANCED":
        data = pd.read_csv("vscodeiitcuoff.csv")
        data["Closing Rank"] = pd.to_numeric(data["Closing Rank"], errors='coerce')
        new_data = data[data["Category"] == category]
        filtered_data = new_data[(new_data["Closing Rank"] > lower) & (new_data["Closing Rank"] < upper)]

        if gender == "Female":
            gender = "Female-only (including Supernumerary)"

        ai_data = filtered_data[(filtered_data["Seat type"] == "AI") & (filtered_data["Gender"] == gender)]
        ai_data = ai_data.sort_values("Closing Rank")
        ai_data.reset_index(drop=True, inplace=True)
        ai_data.index += 1
        result_df = ai_data

    if not result_df.empty:
        st.dataframe(result_df, use_container_width=True)

        buffer = BytesIO()
        result_df.to_csv(buffer, index=True)
        buffer.seek(0)

        st.download_button(
            label="Download Filtered Data as CSV",
            data=buffer,
            file_name="filtered_cutoff_data.csv",
            mime="text/csv"
        )
    else:
        st.warning("No data found for the given criteria.")
