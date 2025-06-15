# 1_Login.py

import streamlit as st

# This must be the first Streamlit command on the page
st.set_page_config(page_title="Login", layout="centered")

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Hardcoded credentials (for demo purposes)
CREDENTIALS = {
    "admin": "password123",
    "rahul": "tiwari@2025"
}

st.title("🔐 Login Page")

# Login Form
with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.form_submit_button("Login")

    if login_button:
        if username in CREDENTIALS and CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.success("Login successful ✅")
            st.rerun()
        else:
            st.error("Invalid username or password ❌")

# Display message after login
if st.session_state.logged_in:
    st.success(f"Welcome, {username}!")
    st.info("Go to the next page using the sidebar ➡️")
