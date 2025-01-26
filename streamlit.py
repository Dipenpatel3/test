import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Retrieve values from environment variables
FAST_API_URL = os.getenv("FAST_API_URL")
REGISTER_URL = f"{FAST_API_URL}/register"
LOGIN_URL = f"{FAST_API_URL}/login"

# Streamlit front-end for user registration
def register_user():
    st.header("Register User")

    # User registration form
    username = st.text_input("Username")
    email_id = st.text_input("Email ID")
    password = st.text_input("Password", type="password")
    
    if st.button("Register"):
        if username and email_id and password:
            try:
                response = requests.post(REGISTER_URL, json={"username": username, "email_id": email_id, "password": password})
                if response.status_code == 200:
                    st.success("User registered successfully!")
                else:
                    st.error(response.json().get("detail", "Something went wrong"))
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Please fill in all fields")

# Streamlit front-end for user login
def login_user():
    st.header("Login User")

    # User login form
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username and password:
            try:
                response = requests.post(LOGIN_URL, json={"username": username, "password": password})
                if response.status_code == 200:
                    st.success("Login successful!")
                else:
                    st.error(response.json().get("detail", "Invalid username or password"))
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Please fill in all fields")

# Main function to switch between Register and Login
def main():
    st.title("User Authentication")
    
    choice = st.sidebar.selectbox("Choose an option", ["Register", "Login"])

    if choice == "Register":
        register_user()
    elif choice == "Login":
        login_user()

if __name__ == "__main__":
    main()
