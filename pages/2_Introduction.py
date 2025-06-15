# pages/2_Introduction.py

import streamlit as st

# Ensure login before proceeding
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first from the Login Page.")
    st.stop()

st.set_page_config(page_title="Introduction", layout="wide")

st.title("📊 Predictive Data Modeling Project")
st.subheader("🚀 Objective:")
st.markdown("""
This application walks through a complete data science pipeline:
1. Uploading and combining raw data
2. Performing Exploratory Data Analysis (EDA)
3. Cleaning and preprocessing data
4. Training a **Logistic Regression** model
5. Making predictions using the trained model

You'll be able to:
- Understand the structure of your data
- Preprocess it properly
- Train and evaluate a model
- Predict success or failure using custom inputs
""")

st.subheader("🗂️ Dataset Info:")
st.markdown("""
- **Train Dataset**: Used for model training and testing.
- **Test Dataset**: For future inference after cleaning and combining.
- The dataset includes a mix of:
  - **Categorical features** (e.g., gender, job type)
  - **Numerical features** (e.g., age, salary)
  - **Target variable**: Binary outcome (Success/Failure)
""")

st.info("Use the sidebar to proceed to Page 3: Data Loading ➡️")
