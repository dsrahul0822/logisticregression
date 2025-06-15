# pages/8_Prediction.py

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

st.set_page_config(page_title="Prediction", layout="wide")

# ✅ Require login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first from the Login Page.")
    st.stop()

st.title("🔮 Prediction Interface")

# Step 1: Load model and features
model_path = "models/model.pkl"
features_path = "models/features.pkl"

if not os.path.exists(model_path) or not os.path.exists(features_path):
    st.error("❌ Model or feature file not found. Please train the model first.")
    st.stop()

with open(model_path, "rb") as f:
    model = pickle.load(f)

with open(features_path, "rb") as f:
    feature_list = pickle.load(f)

st.success("✅ Model and feature list loaded successfully!")

# Step 2: Create input form dynamically based on features
st.subheader("📝 Enter Input Values for Prediction")

input_data = {}

with st.form("prediction_form"):
    for feature in feature_list:
        val = st.text_input(f"{feature}", key=feature)
        input_data[feature] = val
    submit = st.form_submit_button("Predict")

# Step 3: Predict on submission
if submit:
    try:
        # Convert all input to float (assuming numerical input)
        input_array = np.array([float(input_data[feat]) for feat in feature_list]).reshape(1, -1)

        # Predict probability
        prob = model.predict_proba(input_array)[0][1]  # Probability of class 1

        st.success(f"✅ Predicted Success Probability: `{prob:.4f}`")
        st.info("💡 If probability > 0.5 → likely Success, else likely Failure")

    except ValueError as ve:
        st.error(f"⚠️ Invalid input: {ve}")
    except Exception as e:
        st.error(f"🚨 Something went wrong: {e}")
