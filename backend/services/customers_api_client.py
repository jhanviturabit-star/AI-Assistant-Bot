import requests
from backend.config import BACKEND_URL

# -----------------------------
# Create Customer
# -----------------------------
def create_customer_api(name: str, email: str, phone: int, token: str):
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "c_name": name,
        "c_email": email,
        "phone": phone
    }

    response = requests.post(f"{BACKEND_URL}/customers/create", json=payload, headers=headers)

    if response.status_code not in (200, 201):
        raise Exception(response.text)
    
    return response.json()

# -----------------------------
# Get All Customers
# -----------------------------
def get_all_customers_api(token: str):
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{BACKEND_URL}/customers/", headers=headers)

    if response.status_code not in (200, 201):
        raise Exception(response.text)
    
    return response.json()
