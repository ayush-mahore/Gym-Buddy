from fastapi import FastAPI
from api.routes import users
from backend.core.database import supabase

app = FastAPI()

# app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Gym Buddy API!"}

# --- Add this temporary test route ---
@app.get("/test-db")
def test_db_connection():
    try:
        # Attempt to query a 'users' table
        response = supabase.table("users").select("*").limit(1).execute()
        return {"status": "Connection successful!", "data": response.data}
    except Exception as e:
        return {"status": "Connection failed or table missing", "error": str(e)}