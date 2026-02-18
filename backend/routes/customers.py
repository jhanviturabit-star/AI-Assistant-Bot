# backend/routes/customers.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import uuid
from backend.auth import get_current_user, admin_required
from backend.services.customers_api_client import create_customer_api, get_all_customers_api

router = APIRouter(prefix="/tickets", tags=["tickets"])

# ---------------------
# Pydantic models
# ---------------------

class CreateCustomer(BaseModel):
    name: str
    email: str
    phone: int

# ---------------------
# Routes
# ---------------------

@router.post("/list")
def list_customers(user=Depends(get_current_user)):
    customers = get_all_customers_api(user["token"])
    return {"customers": customers}

@router.post("/create")
def create_customer_route(customer=CreateCustomer, user=Depends(get_current_user)):
    result = create_customer_api(customer.name, customer.email, customer.phone, user["token"])
    print("TOOL EXECUTION ID:", uuid.uuid4())
    return {"message": "Customer created successfully", result:"customer"}

