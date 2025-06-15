# pages/5_EDA.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="EDA", layout="wide")

# ✅ Require login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first from the Login Page.")
    st.stop()

# ✅ Require dataset
if "raw_data" not in st.session_state:
    st.error("❌ No dataset found. Please upload the data first.")
    st.stop()

df = st.session_state.raw_data.copy()
st.title("📊 Exploratory Data Analysis (EDA)")

# Split columns
categorical_cols = df.select_dtypes(include="object").columns.tolist()
numerical_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

# ========== COUNT PLOTS FOR CATEGORICAL FEATURES ==========
st.subheader("📌 Count Plots for Categorical Columns")

if not categorical_cols:
    st.warning("No categorical columns found.")
else:
    selected_cat = st.selectbox("Select a categorical column for count plot", categorical_cols)
    hue_cat = st.selectbox("Select a hue (optional)", ["None"] + categorical_cols)

    fig, ax = plt.subplots()
    if hue_cat != "None":
        sns.countplot(data=df, x=selected_cat, hue=hue_cat, ax=ax)
    else:
        sns.countplot(data=df, x=selected_cat, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# ========== SCATTER PLOTS FOR NUMERICAL FEATURES ==========
st.subheader("📌 Scatter Plots for Numerical Columns")

if len(numerical_cols) < 2:
    st.warning("Need at least 2 numerical columns for scatter plot.")
else:
    x_num = st.selectbox("Select X-axis", numerical_cols, key="x_axis")
    y_num = st.selectbox("Select Y-axis", [col for col in numerical_cols if col != x_num], key="y_axis")
    hue_num = st.selectbox("Select hue (optional)", ["None"] + categorical_cols, key="hue_select")

    fig2, ax2 = plt.subplots()
    if hue_num != "None":
        sns.scatterplot(data=df, x=x_num, y=y_num, hue=hue_num, ax=ax2)
    else:
        sns.scatterplot(data=df, x=x_num, y=y_num, ax=ax2)
    st.pyplot(fig2)
