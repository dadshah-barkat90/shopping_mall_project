import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scripts.analysis import perform_all_analysis
from scripts.extract_data import fetch_data
from scripts.clean_data import clean_data
from scripts.store_sql import store_to_sql

import json

st.set_page_config(page_title="Product Analysis App", layout="wide")

st.title("🛒 Product Analysis Dashboard")
st.write("Analyze product data, clean it, visualize it, and store it.")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Go to", ["Upload & Clean Data", "Analysis", "Visualizations", "Save to SQL"]
)


# Load JSON file
def load_json(file):
    return pd.DataFrame(json.load(file))


if "clean_df" not in st.session_state:
    st.session_state.clean_df = None

# Page 1: Upload & Clean Data
if page == "Upload & Clean Data":
    st.header("📤 Upload JSON File")
    uploaded = st.file_uploader("Upload your product JSON", type="json")

    if uploaded:
        df = load_json(uploaded)
        st.session_state.clean_df = clean_data(df)

        st.subheader("Cleaned Data")
        st.dataframe(st.session_state.clean_df)

# Page 2: Analysis
elif page == "Analysis":
    st.header("📊 Data Insights")

    if st.session_state.clean_df is None:
        st.warning("Upload and clean data first!")
    else:
        insights = perform_all_analysis(st.session_state.clean_df)
        for key, value in insights.items():
            st.write(f"### {key}")
            st.write(value)

# Page 3: Visualizations
elif page == "Visualizations":
    st.header("📈 Visual Graphs")

    if st.session_state.clean_df is None:
        st.warning("Upload data first!")
    else:
        df = st.session_state.clean_df

        # Graph 1: Price distribution
        st.subheader("Price Distribution")
        fig, ax = plt.subplots()
        ax.hist(df["price"])
        st.pyplot(fig)

        # Graph 2: Category counts
        st.subheader("Category Counts")
        fig, ax = plt.subplots()
        df["category"].value_counts().plot(kind="bar", ax=ax)
        st.pyplot(fig)

# Page 4: Save to SQL
elif page == "Save to SQL":
    st.header("💾 Save Clean Data to SQL")

    if st.session_state.clean_df is None:
        st.warning("Upload data first!")
    else:
        if st.button("Save to SQL Database"):
            store_to_sql(st.session_state.clean_df)
            st.success("Data successfully saved to SQL!")
