from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import snowflake.connector

# Initialize FastAPI app
app = FastAPI()

from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Retrieve values from environment variables
snowflake_user = os.getenv("SNOWFLAKE_USER")
snowflake_password = os.getenv("SNOWFLAKE_PASSWORD")
snowflake_account = os.getenv("SNOWFLAKE_ACCOUNT")
snowflake_database = os.getenv("SNOWFLAKE_DATABASE")
snowflake_schema = os.getenv("SNOWFLAKE_SCHEMA")
snowflake_warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
snowflake_table = os.getenv("SNOWFLAKE_TABLE")

def get_db_connection():
    return snowflake.connector.connect(
        user=snowflake_user,
        password=snowflake_password,
        account=snowflake_account,
        warehouse=snowflake_warehouse,
        database=snowflake_database,
        schema=snowflake_schema
    )

# Define request models
class RegisterRequest(BaseModel):
    username: str
    email_id: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/register")
async def register_user(request: RegisterRequest):
    """Register a new user."""
    query = f"""
    INSERT INTO {snowflake_table} (USERNAME, PASSWORD, EMAIL_ID)
    VALUES (%s, %s, %s)
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (request.username, request.password, request.email_id))
            cursor.close()
    except snowflake.connector.errors.IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    return {"message": "User registered successfully"}

@app.post("/login")
async def login_user(request: LoginRequest):
    """Login an existing user."""
    query = f"""
    SELECT PASSWORD FROM {snowflake_table} WHERE USERNAME = %s
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (request.username,))
        result = cursor.fetchone()
        cursor.close()

    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    stored_password = result[0]

    if request.password != stored_password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful"}
