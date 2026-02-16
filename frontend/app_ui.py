import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000" 

st.set_page_config(page_title="CRM AI Assistant", page_icon=" ")

# -----------------------
# Session State Init
# -----------------------
if "token" not in st.session_state:
    st.session_state.token = None

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "Login"

# -----------------------
# Helper Functions
# -----------------------

def login_user(email, password):
    try:
        response = requests.post(
            f"{BACKEND_URL}/login",
            json={"email": email, "password": password},
        )

        if response.status_code == 200:
            data = response.json()
            st.session_state.token = data.get("access_token")
            return True, "Login successful!"
        else:
            return False, response.json().get("detail", "Login failed.")
    except Exception as e:
        return False, str(e)


def signup_user(email, password, role):
    try:
        response = requests.post(
            f"{BACKEND_URL}/signup",
            json={
                "email": email,
                "password": password,
                "role": role
            },
        )

        if response.status_code == 200:
            return True, "Signup successful! Please login."
        else:
            return False, response.json().get("detail", "Signup failed.")
    except Exception as e:
        return False, str(e)


def logout():
    st.session_state.token = None
    st.session_state.auth_mode = "Login"


# -----------------------
# UI Rendering
# -----------------------

st.title("CRM AI Assistant")

if st.session_state.token:

    st.success("You are logged in.")
    st.button("Logout", on_click=logout)

    st.info("You can now access CRM features from other pages.")

else:

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            st.session_state.auth_mode = "Login"

    with col2:
        if st.button("Signup"):
            st.session_state.auth_mode = "Signup"

    st.divider()

    if st.session_state.auth_mode == "Login":

        st.subheader("Login")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Submit Login"):
            success, message = login_user(email, password)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    elif st.session_state.auth_mode == "Signup":

        st.subheader("Signup")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["agent", "admin"])

        if st.button("Submit Signup"):
            success, message = signup_user(email, password, role)
            if success:
                st.success(message)
                st.session_state.auth_mode = "Login"
            else:
                st.error(message)
