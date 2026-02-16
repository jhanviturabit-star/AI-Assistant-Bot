import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Tickets", page_icon=" ")

st.title("Tickets")

# -----------------------------
# Authentication Check
# -----------------------------
if "token" not in st.session_state or not st.session_state.token:
    st.error("You must login first.")
    st.stop()

headers = {
    "Authorization": f"Bearer {st.session_state.token}"
}

# -----------------------------
# Fetch Tickets
# -----------------------------
def fetch_tickets():
    try:
        response = requests.get(
            f"{BACKEND_URL}/tickets/",
            headers=headers
        )

        if response.status_code == 200:
            return response.json(), None

        elif response.status_code == 401:
            return None, "Unauthorized. Please login again."

        elif response.status_code == 403:
            return None, "Forbidden. You do not have permission."

        else:
            return None, f"Error {response.status_code}: {response.text}"

    except Exception as e:
        return None, str(e)


tickets, error = fetch_tickets()

if error:
    st.error(error)
    st.stop()

if not tickets:
    st.info("No tickets found.")
    st.stop()

# -----------------------------
# Convert to DataFrame
# -----------------------------
df = pd.DataFrame(tickets)

# -----------------------------
# Filters Section
# -----------------------------
st.subheader("Filter Tickets")

col1, col2 = st.columns(2)

with col1:
    status_filter = st.selectbox(
        "Status",
        ["All"] + sorted(df["t_status"].dropna().unique().tolist())
    )

with col2:
    priority_filter = st.selectbox(
        "Priority",
        ["All"] + sorted(df["priority"].dropna().unique().tolist())
    )

filtered_df = df.copy()

if status_filter != "All":
    filtered_df = filtered_df[filtered_df["t_status"] == status_filter]

if priority_filter != "All":
    filtered_df = filtered_df[filtered_df["priority"] == priority_filter]

st.divider()

# -----------------------------
# Summary Section
# -----------------------------
st.subheader("Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Total Tickets", len(filtered_df))

if "t_status" in filtered_df.columns:
    open_count = len(filtered_df[filtered_df["t_status"] == "Open"])
    col2.metric("Open Tickets", open_count)

if "priority" in filtered_df.columns:
    high_priority = len(filtered_df[filtered_df["priority"] == "High"])
    col3.metric("High Priority", high_priority)

st.divider()

# -----------------------------
# Tickets Table
# -----------------------------
st.subheader("Ticket List")

st.dataframe(
    filtered_df,
    use_container_width=True
)
