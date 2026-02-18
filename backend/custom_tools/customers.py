import requests
from langchain.tools import tool
from backend.config import BACKEND_URL 
from backend.context import current_token
from backend.services.customers_api_client import create_customer_api, get_all_customers_api

@tool
def get_all_customers(token: str) -> str:
    """Fetch all customers from the CRM dynamically using user's JWT"""
    token = current_token.get()
    result = get_all_customers_api(token)
    return result


@tool
def create_customer(name: str, email: str, phone: int) -> str:
    """Create Customer."""
    token = current_token.get()
    print(repr(phone))
    result = create_customer_api(name=name, email=email, phone=str(phone), token=token)
    return result
