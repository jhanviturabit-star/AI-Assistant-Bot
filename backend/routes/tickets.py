# backend/routes/tickets.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.auth import get_current_user, admin_required
from backend.services.tickets_api_client import create_ticket_api, get_all_tickets_api, reassign_ticket_api, update_ticket_status_api

router = APIRouter(prefix="/tickets", tags=["tickets"])

# ---------------------
# Pydantic models
# ---------------------

class TicketCreate(BaseModel):
    customer_email: str
    title: str
    description: str = ""
    priority: str  # Low / Medium / High

class TicketReassign(BaseModel):
    ticket_id: int
    agent_id: str

class TicketStatusUpdate(BaseModel):
    ticket_id: int
    status: str
    priority: Optional[str] = None

# ---------------------
# Routes
# ---------------------

@router.post("/create")
def create_ticket_route(ticket: TicketCreate, user=Depends(get_current_user)):
    result = create_ticket_api(
        ticket.title,
        ticket.description,
        ticket.priority,
        ticket.customer_email,
        user["token"]
    )
    return {"message": f"Ticket #{result['id']} created successfully."}


@router.get("/list")
def list_tickets(user=Depends(get_current_user)):
    tickets = get_all_tickets_api(user["token"])
    return {"tickets": tickets}


@router.post("/update_status")
def update_ticket_status_route(data: TicketStatusUpdate, user=Depends(get_current_user)):
    updated = update_ticket_status_api(
        data.ticket_id,
        data.status,
        data.priority,
        user["token"]
    )
    return {"ticket": updated}


@router.post("/reassign")
def reassign_ticket_route(data: TicketReassign, user=Depends(admin_required)):
    result = reassign_ticket_api(
        data.ticket_id,
        data.agent_id,
        user["token"]
    )
    return {"ticket": result}


@router.get("/summary")
def ticket_summary(user=Depends(get_current_user)):
    tickets = get_all_tickets_api(user["token"])

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

    return {"summary": summary}