from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.database import supabase

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        # We ask the Supabase client to verify the token. 
        # If valid, it returns the user's data (including their UUID).
        user_response = supabase.auth.get_user(token)
        return user_response.user
        
    except Exception as e:
        # If the token is expired, fake, or missing, we reject the request
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )