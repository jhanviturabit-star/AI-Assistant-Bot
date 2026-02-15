from fastapi import HTTPException, APIRouter
from backend.config import BACKEND_URL
from pydantic import BaseModel
import requests

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

# Request model
class LoginRequest(BaseModel):
    email: str
    password: str

# Response model
class LoginResponse(BaseModel):
    token: str
    role: str
    user_id: int

# Login endpoint
@auth_router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest):  
    """
    Authenticate user from Project1 API & request token + role
    """

    payload = {
        "email": login_data.email,
        "password": login_data.password
    }

    try:
        response = requests.post(f"{BACKEND_URL}/auth/login", json=payload)

        response_data = response.json()

        if response.status_code != 200:
            raise HTTPException(
                status_code=401,
                detail=response_data.get("message", "Invalid credentials")
            )

        return LoginResponse(
            token=response_data["token"],
            role=response_data["role"],
            user_id=response_data["user_id"]
        )

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Login service unreachable: {str(e)}"
        )
