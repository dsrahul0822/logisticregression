# pages/6_Data_Cleaning.py

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title="Data Cleaning", layout="wide")

# ✅ Require login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first from the Login Page.")
    st.stop()

# ✅ Initialize cleaned_df if not already
if "cleaned_df" not in st.session_state:
    if "raw_data" in st.session_state:
        st.session_state.cleaned_df = st.session_state.raw_data.copy()
    else:
        st.error("❌ No raw dataset found. Please upload data first.")
        st.stop()

# ✅ Work with session-state DataFrame
df = st.session_state.cleaned_df

st.title("🧹 Interactive Data Cleaning")

# ===== 1. Missing Value Treatment =====
st.subheader("1️⃣ Missing Value Treatment")

missing_cols = df.columns[df.isnull().any()].tolist()

if missing_cols:
    selected_col = st.selectbox("Select a column with missing values", missing_cols, key="missing_col")

    if pd.api.types.is_numeric_dtype(df[selected_col]):
        method = st.radio("Select method", ["Mean", "Median"], key="missing_method")
        if st.button("Apply Missing Value Treatment"):
            if method == "Mean":
                df[selected_col].fillna(df[selected_col].mean(), inplace=True)
            else:
                df[selected_col].fillna(df[selected_col].median(), inplace=True)
            st.success(f"{method} imputation applied to {selected_col}")
    else:
        if st.button("Apply Mode Imputation"):
            df[selected_col].fillna(df[selected_col].mode()[0], inplace=True)
            st.success(f"Mode imputation applied to {selected_col}")
else:
    st.info("✅ No missing values found.")

# ===== 2. Outlier Treatment =====
st.subheader("2️⃣ Outlier Treatment (1.5 * IQR method)")

numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

if numeric_cols:
    selected_outlier_col = st.selectbox("Select a numerical column for outlier treatment", numeric_cols, key="outlier_col")

    if st.button("Apply IQR Outlier Capping"):
        Q1 = df[selected_outlier_col].quantile(0.25)
        Q3 = df[selected_outlier_col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df[selected_outlier_col] = np.where(df[selected_outlier_col] > upper, upper, df[selected_outlier_col])
        df[selected_outlier_col] = np.where(df[selected_outlier_col] < lower, lower, df[selected_outlier_col])
        st.success(f"Outliers in {selected_outlier_col} capped using IQR method")
else:
    st.info("No numerical columns available for outlier treatment.")

# ===== 3. Encoding Categorical Columns =====
st.subheader("3️⃣ Encoding Categorical Columns")

cat_cols = df.select_dtypes(include="object").columns.tolist()

if cat_cols:
    selected_encode_col = st.selectbox("Select a categorical column to encode", cat_cols, key="encode_col")
    unique_vals = df[selected_encode_col].nunique()

    if unique_vals == 2:
        if st.button("Apply Label Encoding"):
            le = LabelEncoder()
            df[selected_encode_col] = le.fit_transform(df[selected_encode_col])
            st.success(f"Label encoding applied to {selected_encode_col}")
    else:
        if st.button("Apply One-Hot Encoding"):
            onehot = pd.get_dummies(df[selected_encode_col], prefix=selected_encode_col,dtype=int, drop_first=True)
            df.drop(selected_encode_col, axis=1, inplace=True)
            df = pd.concat([df, onehot], axis=1)
            st.success(f"One-hot encoding applied to {selected_encode_col}")
else:
    st.info("✅ No categorical columns found.")

# ====== Preview & Save ======
st.subheader("📄 Cleaned Data Preview")
st.dataframe(df.head())

st.session_state.cleaned_df = df  # Save back the updated df
st.info("🎯 Proceed to Page 7: Model Training ➡️")
