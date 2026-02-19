import streamlit as st
import requests

# -------------------------
# CONFIG
# -------------------------
BACKEND_URL = "http://localhost:8000" 

st.set_page_config(
    page_title="CRM AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.markdown(
    """
    <h1 style='text-align: center;'>🤖 CRM AI Assistant</h1>
    <p style='text-align: center; color: grey;'>
        Interact with tickets & customers using natural language
    </p>
    """,
    unsafe_allow_html=True
)

# -----------------------
# Session State Init
# -----------------------
if "token" not in st.session_state:
    st.session_state.token = None

if "role" not in st.session_state:
    st.session_state.role = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------
# LOGIN FUNCTION
# -------------------------
def login(email, password):
    response = requests.post(
        f"{BACKEND_URL}/auth/login",
        json={"email": email, "password": password}
    )

    if response.status_code == 200:
        data = response.json()
        st.session_state.token = data["token"]
        st.session_state.role = data["role"]
        st.success("Login successful")
        st.rerun()
    else:
        st.error("Invalid credentials")

# -------------------------
# SEND MESSAGE FUNCTION
# -------------------------
def send_message(message):
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    response = requests.post(
        f"{BACKEND_URL}/chat",
        json={"message": message},
        headers=headers
    )

    if response.status_code == 200:
        return response.json().get("response", "No response")
    else:
        return f"Error: {response.text}"

# -------------------------
# LOGIN SCREEN
# -------------------------
if not st.session_state.token:
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        login(email, password)

# -------------------------
# CHAT SCREEN
# -------------------------
else:
    st.sidebar.success(f"Logged in as: {st.session_state.role.upper()}")

    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.role = None
        st.session_state.chat_history = []
        st.rerun()

    st.subheader("Chat with your CRM Assistant")

    # Display previous messages
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask something about tickets or customers...")

    if user_input:
        # Add user message
        st.session_state.chat_history.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        # Get AI response
        ai_response = send_message(user_input)

        # Add AI message
        st.session_state.chat_history.append(
            {"role": "assistant", "content": ai_response}
        )

        with st.chat_message("assistant"):
            st.markdown(ai_response)
