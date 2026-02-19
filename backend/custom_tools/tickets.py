from langchain.tools import tool
import requests
import json
from backend.config import BACKEND_URL, PROJECT1_JWT_SECRET_KEY  
from typing import Optional
import jwt
from backend.context import current_token
from backend.services.tickets_api_client import create_ticket_api, get_all_tickets_api, update_ticket_status_api, reassign_ticket_api

@tool
def get_all_tickets() -> dict:
    """Fetch all tickets from the CRM dynamically using user's JWT"""
    token = current_token.get()
    return get_all_tickets_api(token)


@tool
def create_ticket(title: str, description: str, priority: str, customer_id: int) -> dict:
    """create ticket."""
    token = current_token.get()
    return create_ticket_api(title, description, priority, customer_id, token)
    

# =====================================================
# ADVANCED AI TICKET TOOLS (Filtered / Summary / Update)
# =====================================================

# -----------------------------
# Filtered Ticket Query
# -----------------------------
@tool
def get_filtered_tickets(
    email: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None) -> dict:
    """
    Fetch tickets filtered by customer email, status or priority.
    """
    token = current_token.get()
    tickets = get_all_tickets_api(token)

    if not isinstance(tickets, list):
        return {'error': tickets}
    
    filtered = []

    for t in tickets:
        if status and t.get("t_status", "").lower() != status.lower():
            continue

        if priority and t.get("priority", "").lower() != status.lower():
            continue

        if email and t.get("email", "").lower() != status.lower():
            continue

        filtered.append(t)

        return {
            "count": len(filtered),
            "tickets": filtered
        }
    
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
    
    return update_ticket_status_api(ticket_id, status, priority, token)

@tool
def reassign_ticket(ticket_id: int, new_agent_id: int) -> dict:
    """
    Reassign a ticket to another agent (admin only)
    """
    token = current_token.get()

    return reassign_ticket_api(ticket_id, new_agent_id, token)
