import requests
from langchain.tools import tool
from config import BACKEND_URL  # your Flask base URL from env

@tool
def get_all_tickets(token: str) -> str:
    """Fetch all tickets from the CRM dynamically using user's JWT"""
    headers = {"Authorization": token}

    response = requests.get(f"{BACKEND_URL}/tickets/", headers=headers)
    return str(response.json())


@tool
def create_ticket(title: str, description: str, priority: str, customer_id: int, token: str) -> str:
    """create ticket."""
    headers = {"Authorization": token}
    payload = {
        "t_title": title,
        "t_description": description,
        "priority": priority,
        "c_id": customer_id
    }
    response = requests.post(f"{BACKEND_URL}/tickets/", json=payload, headers=headers)
    return str(response.json())



# FLASK_BASE_URL = "http://127.0.0.1:5000"  # your Flask port

# TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNSwicm9sZSI6IkFHRU5UIiwiZXhwIjoxNzcwOTIxOTUzfQ.u_YC12MYaA2Tvugkalj6DxaTr8kEB-Ceeyqn1BwpZ9Y"

# @tool
# def get_tickets(token:str) -> str:
#     """
#     Fetch all tickets from the CRM.
#     Expects `token` as the Authorization header.
#     """
#     headers = {
#         "Authorization": token
#     }
#     response = requests.get(f"{FLASK_BASE_URL}/tickets/", headers=headers)

#     return str(response.json())
