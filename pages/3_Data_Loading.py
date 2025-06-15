# pages/3_Data_Loading.py

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Loading", layout="wide")

# ✅ Require login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first from the Login Page.")
    st.stop()

st.title("📂 Upload Combined Dataset")

# ✅ File Uploader (combined data)
combined_file = st.file_uploader("Upload Combined CSV Dataset", type=["csv"], key="combined_upload")

if combined_file is not None:
    df = pd.read_csv(combined_file)
    st.session_state.raw_data = df  # Store raw dataset in session
    st.success(f"✅ Dataset loaded with shape: {df.shape}")

    # ✅ Preview
    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head())

    # ✅ Show column types
    st.subheader("📊 Column Information")
    st.write(df.dtypes)

    st.info("✅ Proceed to Page 4: Combine Data ➡️ (if needed)")
else:
    st.info("📤 Please upload a CSV file to continue.")
