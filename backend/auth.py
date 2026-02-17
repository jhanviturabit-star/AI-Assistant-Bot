from fastapi import HTTPException, APIRouter, Depends
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.config import BACKEND_URL, PROJECT1_JWT_SECRET_KEY
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
    token = credentials.credentials

    try:
        payload = jwt.decode(token, PROJECT1_JWT_SECRET_KEY, algorithms = ["HS256"])

        user_id = payload.get("user_id")
        role = payload.get("role")

        if user_id is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return {
            "user_id": user_id,
            "role": role,
            "token": token
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="invalid or expired token")


def admin_required(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Ensure the user is an admin
    """
    user = get_current_user(credentials)
    if user.get[("role").upper] != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user
