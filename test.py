import snowflake.connector
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
# Establish a connection
try:
    conn = snowflake.connector.connect(
        user=snowflake_user,
        password=snowflake_password,
        account=snowflake_account,
        warehouse=snowflake_warehouse,
        database=snowflake_database,
        schema=snowflake_schema
    )
    print("Connection established successfully!")
    
    # Your Snowflake queries go here...
    
except Exception as e:
    print(f"Failed to connect to Snowflake: {e}")
