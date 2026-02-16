# backend/routes/tickets.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from backend.auth import get_current_user, admin_required
from backend.custom_tools import create_ticket, get_filtered_tickets, update_ticket_status, reassign_ticket

router = APIRouter(prefix="/tickets", tags=["tickets"])

class TicketCreate(BaseModel):
    customer_email: str
    title: str
    description: str = ""
    priority: str  # Low / Medium / High

class TicketReassign(BaseModel):
    ticket_id: int
    agent_id: str

@router.post("/create")
def create_ticket_route(ticket: TicketCreate, user=Depends(get_current_user)):
    """Create a new ticket"""
    result = create_ticket(ticket.customer_email, ticket.title, ticket.description, ticket.priority)
    return {"message": f"Ticket #{result['id']} created successfully."}

@router.get("/list")
def list_tickets(customer_email: str = None, user=Depends(get_current_user)):
    """List tickets (optional filter by customer)"""
    tickets = get_filtered_tickets(customer_email=customer_email)
    return {"tickets": tickets}

@router.post("/update_status")
def update_ticket_status_route(ticket_id: int, status: str, user=Depends(get_current_user)):
    """Update ticket status"""
    updated = update_ticket_status(ticket_id, status)
    return {"message": f"Ticket #{ticket_id} status updated to {status}"}

@router.post("/reassign")
def reassign_ticket_route(data: TicketReassign, user=Depends(admin_required)):
    """Reassign a ticket to another agent (admin only)"""
    result = reassign_ticket(data.ticket_id, data.agent_id)
    return {"message": result}
