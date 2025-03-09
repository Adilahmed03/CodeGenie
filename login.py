import streamlit as st
import hashlib
import json
import os
from datetime import datetime, timedelta

# Function to create user database file if it doesn't exist
def initialize_user_database():
    if not os.path.exists("users"):
        os.makedirs("users")
    
    if not os.path.exists("users/user_database.json"):
        users = {
            "admin": {
                "password": hashlib.sha256("admin123".encode()).hexdigest(),
                "email": "admin@codegenie.com",
                "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "last_login": None
            }
        }
        with open("users/user_database.json", "w") as f:
            json.dump(users, f, indent=4)

# Function to authenticate user
def authenticate_user(username, password):
    try:
        with open("users/user_database.json", "r") as f:
            users = json.load(f)
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        if username in users and users[username]["password"] == hashed_password:
            # Update last login
            users[username]["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("users/user_database.json", "w") as f:
                json.dump(users, f, indent=4)
            return True
        return False
    except Exception as e:
        st.error(f"Authentication error: {e}")
        return False

# Function to register new user
def register_user(username, password, email):
    try:
        # Load existing users
        with open("users/user_database.json", "r") as f:
            users = json.load(f)
        
        # Check if username already exists
        if username in users:
            return False, "Username already exists"
        
        # Check if email is already in use
        for user in users.values():
            if user["email"] == email:
                return False, "Email already in use"
        
        # Add new user
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        users[username] = {
            "password": hashed_password,
            "email": email,
            "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_login": None
        }
        
        # Save updated users
        with open("users/user_database.json", "w") as f:
            json.dump(users, f, indent=4)
        
        return True, "Registration successful"
    except Exception as e:
        return False, f"Registration error: {e}"

# Function for reset password
def reset_password(email, new_password):
    try:
        # Load existing users
        with open("users/user_database.json", "r") as f:
            users = json.load(f)
        
        # Find user with matching email
        username_found = None
        for username, user_data in users.items():
            if user_data["email"] == email:
                username_found = username
                break
        
        if username_found:
            # Update password
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            users[username_found]["password"] = hashed_password
            
            # Save updated users
            with open("users/user_database.json", "w") as f:
                json.dump(users, f, indent=4)
            
            return True, "Password reset successful"
        else:
            return False, "Email not found"
    except Exception as e:
        return False, f"Password reset error: {e}"

# Login page UI
def login_page():
    initialize_user_database()
    
    # Set page configuration
    st.set_page_config(
        page_title="CodeGenie - Login",
        page_icon="🧞‍♂️",
        layout="wide"
    )
    
    # Create three columns for centering the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("🧞‍♂️ CodeGenie")
        st.markdown("### AI-Powered Code Generation")
        
        # Tabs for login and registration
        login_tab, register_tab, reset_tab = st.tabs(["Login", "Register", "Reset Password"])
        
        with login_tab:
            st.subheader("Login to your account")
            
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", key="login_button"):
                if username and password:
                    if authenticate_user(username, password):
                        st.success("Login successful!")
                        # Store in session state
                        st.session_state["authenticated"] = True
                        st.session_state["username"] = username
                        # Add a rerun to refresh the page
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.warning("Please enter both username and password")
        
        with register_tab:
            st.subheader("Create a new account")
            
            new_username = st.text_input("Choose Username", key="reg_username")
            new_email = st.text_input("Email", key="reg_email")
            new_password = st.text_input("Create Password", type="password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
            
            if st.button("Register", key="register_button"):
                if new_username and new_email and new_password and confirm_password:
                    if new_password != confirm_password:
                        st.error("Passwords do not match")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters long")
                    elif "@" not in new_email or "." not in new_email:
                        st.error("Please enter a valid email address")
                    else:
                        success, message = register_user(new_username, new_password, new_email)
                        if success:
                            st.success(message)
                            st.info("You can now login with your new account")
                        else:
                            st.error(message)
                else:
                    st.warning("Please fill in all fields")
        
        with reset_tab:
            st.subheader("Reset your password")
            
            reset_email = st.text_input("Enter your email", key="reset_email")
            reset_new_password = st.text_input("New Password", type="password", key="reset_new_pass")
            reset_confirm_password = st.text_input("Confirm New Password", type="password", key="reset_confirm")
            
            if st.button("Reset Password", key="reset_button"):
                if reset_email and reset_new_password and reset_confirm_password:
                    if reset_new_password != reset_confirm_password:
                        st.error("Passwords do not match")
                    elif len(reset_new_password) < 6:
                        st.error("Password must be at least 6 characters long")
                    else:
                        success, message = reset_password(reset_email, reset_new_password)
                        if success:
                            st.success(message)
                            st.info("You can now login with your new password")
                        else:
                            st.error(message)
                else:
                    st.warning("Please fill in all fields")

# Main function to integrate login with the CodeGenie application
def main():
    # Check if user is authenticated
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    # If not authenticated, show login page
    if not st.session_state["authenticated"]:
        login_page()
    else:
        # Here we would import and run the main CodeGenie application
        # For demonstration, we'll just show a placeholder
        
        # Set page configuration (same as original)
        st.set_page_config(
            page_title="CodeGenie - AI Code Generation",
            page_icon="🧞‍♂️",
            layout="wide"
        )
        
        # Header with logout option
        col1, col2 = st.columns([3, 1])
        with col1:
            st.title("🧞‍♂️ CodeGenie")
            st.markdown(f"### Welcome, {st.session_state['username']}!")
        with col2:
            if st.button("Logout"):
                st.session_state["authenticated"] = False
                st.session_state.pop("username", None)
                st.rerun()
        
        # Here you would import and include the original CodeGenie code
        # For example:
        # from codegenie import run_codegenie_app
        # run_codegenie_app()
        
        # Placeholder for demonstration
        st.success("You are now logged in! The original CodeGenie application would be loaded here.")
        st.info("This is a placeholder. In a real implementation, you would load the original CodeGenie code here.")

if __name__ == "__main__":
    main()
