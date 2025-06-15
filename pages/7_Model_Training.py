# pages/7_Model_Training.py

import streamlit as st
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import os

st.set_page_config(page_title="Model Training", layout="wide")

# ✅ Require login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first from the Login Page.")
    st.stop()

# ✅ Require cleaned dataset
if "cleaned_df" not in st.session_state:
    st.error("❌ No cleaned data found. Please finish cleaning first.")
    st.stop()

df = st.session_state.cleaned_df.copy()
st.title("🧠 Model Training – Logistic Regression")

# Step 1: Select target column
target_col = st.selectbox("🎯 Select the target column", df.columns)

# Step 2: Select columns to drop (e.g., ID columns)
feature_cols = [col for col in df.columns if col != target_col]
cols_to_drop = st.multiselect("🧹 Select columns to exclude from training (like IDs)", feature_cols)

# Step 3: Train model
if st.button("Train Model"):
    try:
        # Create features and target
        X = df.drop(columns=[target_col] + cols_to_drop)
        y = df[target_col]

        # Split into train/test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train model
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)

        # Save model and features
        os.makedirs("models", exist_ok=True)
        with open("models/model.pkl", "wb") as f:
            pickle.dump(model, f)
        with open("models/features.pkl", "wb") as f:
            pickle.dump(X.columns.tolist(), f)

        st.success("✅ Model trained and saved!")
        st.write(f"📊 Train Accuracy: {model.score(X_train, y_train):.4f}")
        st.write(f"📊 Test Accuracy: {model.score(X_test, y_test):.4f}")

    except Exception as e:
        st.error(f"🚨 Error during training: {e}")
