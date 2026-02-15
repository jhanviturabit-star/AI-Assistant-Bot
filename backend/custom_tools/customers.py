import requests
from langchain.tools import tool
from backend.config import BACKEND_URL 

@tool
def get_all_customers(token: str) -> str:
    """Fetch all customers from the CRM dynamically using user's JWT"""
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{BACKEND_URL}/customers/", headers=headers)
    return str(response.json())


@tool
def create_customer(name: str, email: str, phone: int, token: str) -> str:
    """create customer."""
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "c_name": name,
        "c_email": email,
        "phone": phone
    }
    response = requests.post(f"{BACKEND_URL}/customers/", json=payload, headers=headers)
    return str(response.json())
