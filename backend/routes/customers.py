# backend/routes/tickets.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from backend.auth import get_current_user, admin_required
from backend.custom_tools import (
    create_ticket,
    get_filtered_tickets,
    update_ticket_status,
    reassign_ticket,
    get_ticket_summary
)

router = APIRouter(prefix="/tickets", tags=["tickets"])

# ---------------------
# Pydantic models
# ---------------------

class TicketCreate(BaseModel):
    customer_email: str
    title: str
    description: Optional[str] = ""
    priority: str  # Low / Medium / High

class TicketReassign(BaseModel):
    ticket_id: int
    agent_id: str

class TicketStatusUpdate(BaseModel):
    ticket_id: int
    status: str  # Open / In Progress / Closed / Resolved

# ---------------------
# Routes
# ---------------------

@router.post("/create")
def create_ticket_route(ticket: TicketCreate, user=Depends(get_current_user)):
    """
    Create a new ticket
    """
    result = create_ticket(ticket.customer_email, ticket.title, ticket.description, ticket.priority)
    return {"message": f"Ticket #{result['id']} created successfully.", "ticket": result}

@router.get("/list")
def list_tickets(customer_email: Optional[str] = None, priority: Optional[str] = None, status: Optional[str] = None, user=Depends(get_current_user)):
    """
    List tickets, optionally filtered by customer, priority, or status
    """
    tickets = get_filtered_tickets(customer_email=customer_email, priority=priority, status=status)
    return {"tickets": tickets}

@router.post("/update_status")
def update_ticket_status_route(data: TicketStatusUpdate, user=Depends(get_current_user)):
    """
    Update the status of a ticket
    """
    updated = update_ticket_status(data.ticket_id, data.status)
    return {"message": f"Ticket #{data.ticket_id} status updated to {data.status}", "ticket": updated}

@router.post("/reassign")
def reassign_ticket_route(data: TicketReassign, user=Depends(admin_required)):
    """
    Reassign a ticket to another agent (admin only)
    """
    result = reassign_ticket(data.ticket_id, data.agent_id)
    return {"message": result}

@router.get("/summary")
def ticket_summary(user=Depends(get_current_user)):
    """
    Get ticket statistics / summary (like total open, closed, etc.)
    """
    summary = get_ticket_summary()
    return {"summary": summary}
