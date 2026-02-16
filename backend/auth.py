from fastapi import HTTPException, APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.config import BACKEND_URL
from pydantic import BaseModel
import requests

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

security = HTTPBearer()

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

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Extract and validate the user from the bearer token via Project1 API
    """
    raw_token = credentials.credentials
    if raw_token.startswith("Bearer "):
        raw_token = raw_token.replace("Bearer ", "")

    try:
        response = requests.get(f"{BACKEND_URL}/auth/me", headers={"Authorization": f"Bearer {raw_token}"})
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return response.json()  # should return user info with id, role, email, etc.
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail="Authentication service unreachable")


def admin_required(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Ensure the user is an admin
    """
    user = get_current_user(credentials)
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user
