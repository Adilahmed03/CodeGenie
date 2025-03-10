import streamlit as st
import hashlib
import json
import os
from datetime import datetime, timedelta
import time
import random
from streamlit_lottie import st_lottie
import requests
import streamlit.components.v1 as components

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

# Function to load Lottie animations
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

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

# Custom CSS for styling
def load_css():
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .main, .main-bg {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    
    h1, h2, h3 {
        color: #00fff5;
        font-weight: 600;
        text-align: center;
        margin-bottom: 20px;
    }
    
    .centered-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
        max-width: 600px;
        margin: 0 auto;
    }
    
    .st-bx {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        backdrop-filter: blur(10px);
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        width: 100%;
        margin: 20px auto;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        border: none;
        color: white;
        flex-grow: 1;
        text-align: center;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(0, 255, 245, 0.1);
        border-bottom: 2px solid #00fff5;
    }
    
    .stButton>button {
        background-color: #e94560;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 8px 20px;
        font-weight: 500;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 10px;
    }
    
    .stButton>button:hover {
        background-color: #ff2e63;
        transform: translateY(-2px);
        box-shadow: 0 8px 16px 0 rgba(233, 69, 96, 0.3);
    }
    
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.05);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 5px;
        padding: 10px 15px;
    }
    
    .success-msg {
        animation: fadeIn 1s ease-in;
        text-align: center;
    }
    
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    /* Floating animation for the logo with smooth border */
    .floating {
        animation: floating 3s ease-in-out infinite;
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
    }
    
    /* Add smooth border to Lottie animation */
    .floating > div {
        border-radius: 15px;
        overflow: hidden;
    }
    
    @keyframes floating {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    /* Typing animation for subtitle - modified to remove hover box */
    .typing-animation {
        overflow: hidden;
        white-space: nowrap;
        border-right: 3px solid #00fff5;
        width: 0;
        margin: 0 auto;
        animation: typing 3s steps(40) 1s forwards, blink 1s step-end infinite;
        background: transparent;
    }
    
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    
    @keyframes blink {
        50% { border-color: transparent }
    }
    
    /* Card effect for login form - removed hover transform */
    .card-effect {
        transition: all 0.3s ease;
    }
    
    /* Center content in tabs */
    .stTabs [data-baseweb="tab-panel"] {
        padding: 15px 0;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        color: rgba(255,255,255,0.5);
        margin-top: 20px;
        padding: 10px;
    }
    
    /* Even spacing for form elements */
    .form-spacing > div {
        margin-bottom: 15px;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Particle animation for background
def load_particles():
    particles_js = """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/particles.js/2.0.0/particles.min.js"></script>
    <div id="particles-js" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;"></div>
    <script>
        particlesJS("particles-js", {
            "particles": {
                "number": {
                    "value": 80,
                    "density": {
                        "enable": true,
                        "value_area": 800
                    }
                },
                "color": {
                    "value": "#00fff5"
                },
                "shape": {
                    "type": "circle",
                    "stroke": {
                        "width": 0,
                        "color": "#000000"
                    },
                    "polygon": {
                        "nb_sides": 5
                    }
                },
                "opacity": {
                    "value": 0.5,
                    "random": true,
                    "anim": {
                        "enable": true,
                        "speed": 1,
                        "opacity_min": 0.1,
                        "sync": false
                    }
                },
                "size": {
                    "value": 3,
                    "random": true,
                    "anim": {
                        "enable": true,
                        "speed": 2,
                        "size_min": 0.1,
                        "sync": false
                    }
                },
                "line_linked": {
                    "enable": true,
                    "distance": 150,
                    "color": "#00fff5",
                    "opacity": 0.4,
                    "width": 1
                },
                "move": {
                    "enable": true,
                    "speed": 2,
                    "direction": "none",
                    "random": false,
                    "straight": false,
                    "out_mode": "out",
                    "bounce": false,
                    "attract": {
                        "enable": false,
                        "rotateX": 600,
                        "rotateY": 1200
                    }
                }
            },
            "interactivity": {
                "detect_on": "canvas",
                "events": {
                    "onhover": {
                        "enable": true,
                        "mode": "repulse"
                    },
                    "onclick": {
                        "enable": true,
                        "mode": "push"
                    },
                    "resize": true
                },
                "modes": {
                    "grab": {
                        "distance": 140,
                        "line_linked": {
                            "opacity": 1
                        }
                    },
                    "bubble": {
                        "distance": 400,
                        "size": 40,
                        "duration": 2,
                        "opacity": 8,
                        "speed": 3
                    },
                    "repulse": {
                        "distance": 100,
                        "duration": 0.4
                    },
                    "push": {
                        "particles_nb": 4
                    },
                    "remove": {
                        "particles_nb": 2
                    }
                }
            },
            "retina_detect": true
        });
    </script>
    """
    components.html(particles_js, height=0)

# Login page UI
def login_page():
    initialize_user_database()
    
    # Set page configuration
    st.set_page_config(
        page_title="CodeGenie - Login",
        page_icon="🧞‍♂️",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Load custom CSS
    load_css()
    
    # Load particles.js for background
    load_particles()
    
    # Load Lottie animations
    lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
    
    # Container for centered content
    st.markdown('<div class="centered-container">', unsafe_allow_html=True)
    
    # Animated logo and title section
    st.markdown('<div class="floating">', unsafe_allow_html=True)
    st_lottie(lottie_coding, height=180, key="coding")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Title without glow effect
    st.markdown('<h1 style="font-size: 2.5rem; margin-bottom: 5px;">🧞‍♂️ CodeGenie</h1>', unsafe_allow_html=True)
    st.markdown('<div class="typing-animation" style="max-width: 300px;"><h3 style="font-size: 1.2rem;">AI-Powered Code Generation</h3></div>', unsafe_allow_html=True)
    
    # Wrap the form in a card without hover effect
    # st.markdown('<div class="st-bx card-effect form-spacing">', unsafe_allow_html=True)
    
    # Tabs for login and registration
    login_tab, register_tab, reset_tab = st.tabs(["Login", "Register", "Reset Password"])
    
    with login_tab:
        st.subheader("Access Your Magic ✨")
        
        username = st.text_input("Username", key="login_username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
        
        if st.button("Login", key="login_button"):
            with st.spinner("Authenticating..."):
                time.sleep(1)  # Simulate loading
                if username and password:
                    if authenticate_user(username, password):
                        st.balloons()
                        st.markdown('<div class="success-msg">', unsafe_allow_html=True)
                        st.success("Login successful! Redirecting...")
                        st.markdown('</div>', unsafe_allow_html=True)
                        # Store in session state
                        st.session_state["authenticated"] = True
                        st.session_state["username"] = username
                        # Add a progress bar before redirect
                        progress_bar = st.progress(0)
                        for percent_complete in range(100):
                            time.sleep(0.01)
                            progress_bar.progress(percent_complete + 1)
                        # Add a rerun to refresh the page
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.warning("Please enter both username and password")
    
    with register_tab:
        st.subheader("Join the Magic Circle 🪄")
        
        new_username = st.text_input("Choose Username", key="reg_username", placeholder="Create a unique username")
        new_email = st.text_input("Email", key="reg_email", placeholder="Enter your email address")
        new_password = st.text_input("Create Password", type="password", key="reg_password", placeholder="Min. 6 characters")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="Re-enter password")
        
        if st.button("Register", key="register_button"):
            with st.spinner("Creating your account..."):
                time.sleep(1.5)  # Simulate loading
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
                            st.balloons()
                            st.markdown('<div class="success-msg">', unsafe_allow_html=True)
                            st.success(message)
                            st.info("You can now login with your new account")
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            st.error(message)
                else:
                    st.warning("Please fill in all fields")
    
    with reset_tab:
        st.subheader("Recover Your Magic 🔮")
        
        reset_email = st.text_input("Enter your email", key="reset_email", placeholder="Your registered email")
        reset_new_password = st.text_input("New Password", type="password", key="reset_new_pass", placeholder="Min. 6 characters")
        reset_confirm_password = st.text_input("Confirm New Password", type="password", key="reset_confirm", placeholder="Re-enter new password")
        
        if st.button("Reset Password", key="reset_button"):
            with st.spinner("Resetting password..."):
                time.sleep(1)  # Simulate loading
                if reset_email and reset_new_password and reset_confirm_password:
                    if reset_new_password != reset_confirm_password:
                        st.error("Passwords do not match")
                    elif len(reset_new_password) < 6:
                        st.error("Password must be at least 6 characters long")
                    else:
                        success, message = reset_password(reset_email, reset_new_password)
                        if success:
                            st.markdown('<div class="success-msg">', unsafe_allow_html=True)
                            st.success(message)
                            st.info("You can now login with your new password")
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            st.error(message)
                else:
                    st.warning("Please fill in all fields")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown('<div class="footer">© 2025 CodeGenie - Your Magical Coding Assistant</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

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
        
        # Set page configuration
        st.set_page_config(
            page_title="CodeGenie - AI Code Generation",
            page_icon="🧞‍♂️",
            layout="centered",
            initial_sidebar_state="collapsed"
        )
        
        # Load custom CSS
        load_css()
        
        # Load particles.js for background
        load_particles()
        
        # Load welcome animation
        lottie_welcome = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_M9p23l.json")
        
        # Container for centered content
        st.markdown('<div class="centered-container">', unsafe_allow_html=True)
        
        # Header with title and welcome message
        st.title("🧞‍♂️ CodeGenie")
        st.markdown(f'<h3>Welcome, <span style="color: #e94560;">{st.session_state["username"]}</span>!</h3>', unsafe_allow_html=True)
        
        # Welcome animation centered
        st_lottie(lottie_welcome, height=250)
        
        # Logout button centered
        if st.button("Logout", key="logout_button"):
            with st.spinner("Logging out..."):
                time.sleep(1)
                st.session_state["authenticated"] = False
                st.session_state.pop("username", None)
                st.rerun()
        
        # Placeholder for demonstration
        st.markdown('<div class="st-bx">', unsafe_allow_html=True)
        st.success("You are now logged in! The original CodeGenie application would be loaded here.")
        st.info("This is a placeholder. In a real implementation, you would load the original CodeGenie code here.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Footer
        st.markdown('<div class="footer">© 2025 CodeGenie - Your Magical Coding Assistant</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()