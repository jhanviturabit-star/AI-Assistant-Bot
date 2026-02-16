from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from backend.config import PROJECT1_JWT_SECRET_KEY

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        decoded = jwt.decode(
            token,
            PROJECT1_JWT_SECRET_KEY,
            algorithms=["HS256"]
        )

        return {
            "decoded": decoded,
            "token": token
        }

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
