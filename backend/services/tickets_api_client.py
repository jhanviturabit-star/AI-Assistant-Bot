import requests
from backend.config import BACKEND_URL

# -----------------------------
# Create Ticket
# -----------------------------
def create_ticket_api(title, description, priority, customer_id, token):
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "t_title": title,
        "t_description": description,
        "priority": priority,
        "c_id": customer_id
    }

    response = requests.post(
        f"{BACKEND_URL}/tickets/create",
        json=payload,
        headers=headers
    )

    if response.status_code not in (200, 201):
        raise Exception(f"Backend Error {response.status_code}: {response.text}")

    return response.json()


# -----------------------------
# Get All Tickets
# -----------------------------
def get_all_tickets_api(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BACKEND_URL}/tickets/", headers=headers)

    if response.status_code not in (200, 201):
        raise Exception(f"Backend Error {response.status_code}: {response.text}")
    
    return response.json()

# -----------------------------
# Update Ticket Status
# -----------------------------
def update_ticket_status_api(ticket_id, status, priority, token: str):
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "t_status": status,
        "priority": priority
    }

    response = requests.patch(
        f"{BACKEND_URL}/tickets/{ticket_id}",
        json=payload,
        headers=headers
    )

    if response.status_code not in (200, 201):
        raise Exception(f"Backend Error {response.status_code}: {response.text}")
    
    return response.json()

# -----------------------------
# Reassign Tickets
# -----------------------------
def reassign_ticket_api(ticket_id, new_agent_id, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"assigned_agent_id": new_agent_id}

    response = requests.patch(
        f"{BACKEND_URL}/tickets/{ticket_id}/{ticket_id}",
        json=payload,
        headers=headers
    )
    
    if response.status_code not in (200, 201):
        raise Exception(f"Backend Error {response.status_code}: {response.text}")
    
    return response.json()