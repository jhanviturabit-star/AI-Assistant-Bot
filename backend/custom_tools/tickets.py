from langchain.tools import tool
import requests
import json
from backend.config import BACKEND_URL, PROJECT1_JWT_SECRET_KEY  
from typing import Optional
import jwt
from backend.context import current_token

@tool
def get_all_tickets() -> dict:
    """Fetch all tickets from the CRM dynamically using user's JWT"""
    token = current_token.get()
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{BACKEND_URL}/tickets/", headers=headers)
    return json.dumps(response.json(), indent=2)


@tool
def create_ticket(title: str, description: str, priority: str, customer_id: int) -> dict:
    """create ticket."""
    token = current_token.get()
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "t_title": title,
        "t_description": description,
        "priority": priority,
        "c_id": customer_id
    }
    response = requests.post(f"{BACKEND_URL}/tickets/", json=payload, headers=headers)
    return json.dumps(response.json(), indent=2)


# =====================================================
# ADVANCED AI TICKET TOOLS (Filtered / Summary / Update)
# =====================================================

# -----------------------------
# Filtered Ticket Query
# -----------------------------
@tool
def get_filtered_tickets(
    status: Optional[str] = None,
    priority: Optional[str] = None) -> dict:
    """
    Fetch tickets filtered by status or priority.
    """
    token = current_token.get()

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{BACKEND_URL}/tickets/", headers=headers)

    data = response.json()

    if response.status_code != 200:
        return {"error": data}

    tickets = data

    # Apply filtering on AI layer
    if status:
        tickets = [t for t in tickets if t.get("t_status") == status]

    if priority:
        tickets = [t for t in tickets if t.get("priority") == priority]

    return json.dumps({
        "count": len(tickets),
        "tickets": tickets
    }, indent=2)


# -----------------------------
# Quick Ticket Summary
# -----------------------------
@tool
def get_ticket_summary() -> dict:
    """
    Return ticket summary grouped by status & priority
    """

    token = current_token.get()

    headers = {"Authorization": f"Bearer {token}"}

    print("Token received:", token)
    
    response = requests.get(f"{BACKEND_URL}/tickets/", headers=headers)

    print("Status:", response.status_code)
    print("Raw response:", response.text)

    if response.status_code != 200:
        return json.dumps({
            "error": f"Backend error {response.status_code}",
            "details": response.text
        }, indent=2)


    try:
        tickets = response.json()
    except Exception:
        return {
            "error": "Invalid JSON from backend",
            "details": response.text
        }   

    summary = {
        "total": len(tickets),
        "by_status": {},
        "by_priority": {}
    }


    for t in tickets:
        status = t.get("t_status")
        priority = t.get("priority")

        summary["by_status"][status] = summary["by_status"].get(status, 0) + 1
        summary["by_priority"][priority] = summary["by_priority"].get(priority, 0) + 1

    return json.dumps(summary, indent=2)


# -----------------------------
# Update Ticket Status / Priority
# -----------------------------
@tool
def update_ticket_status(
    ticket_id: int,
    status: Optional[str] = None,
    priority: Optional[str] = None) -> dict:
    """
    Update ticket status or priority.
    """
    token = current_token.get()
    
    # Decode JWT to extract role & user_id
    try:
        decoded = jwt.decode(token, PROJECT1_JWT_SECRET_KEY, algorithms=["HS256"])
        user_role = decoded.get("role")
        user_id = decoded.get("user_id")
    except Exception:
        return json.dumps({"error": "Invalid token"})

    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "t_status": status,
        "priority": priority,
        "role": user_role,
        "user_id": user_id
    }

    response = requests.patch(
        f"{BACKEND_URL}/tickets/{ticket_id}",
        json=payload,
        headers=headers
    )

    return json.dumps(response.json(), indent=2)
