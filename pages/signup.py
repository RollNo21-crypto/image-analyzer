# pages/signup.py
import streamlit as st
import re
from components.db import create_user, get_user_by_username

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username):
    """Validate username format"""
    # Username should be 3-20 characters, alphanumeric and underscore only
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return re.match(pattern, username) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

def signup_page():
    st.title("🔐 Create Your Account")
    st.markdown("Join the Image Analyzer community!")
    
    with st.form("signup_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name", placeholder="Enter your full name")
            username = st.text_input("Username", placeholder="Choose a unique username")
            
        with col2:
            email = st.text_input("Email", placeholder="your.email@example.com")
            password = st.text_input("Password", type="password", placeholder="Create a strong password")
        
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        
        # Terms and conditions
        agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        
        submit_button = st.form_submit_button("Create Account", use_container_width=True)
        
        if submit_button:
            # Validation
            errors = []
            
            if not full_name.strip():
                errors.append("Full name is required")
            
            if not validate_username(username):
                errors.append("Username must be 3-20 characters long and contain only letters, numbers, and underscores")
            
            if not validate_email(email):
                errors.append("Please enter a valid email address")
            
            is_valid_password, password_message = validate_password(password)
            if not is_valid_password:
                errors.append(password_message)
            
            if password != confirm_password:
                errors.append("Passwords do not match")
            
            if not agree_terms:
                errors.append("You must agree to the Terms of Service")
            
            # Check if username already exists
            if validate_username(username) and get_user_by_username(username):
                errors.append("Username already exists")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Create the user
                success, message = create_user(username, email, password, full_name)
                
                if success:
                    st.success("🎉 Account created successfully!")
                    st.info("You can now log in with your credentials")
                    st.balloons()
                    # Set a flag to show the login button outside the form
                    st.session_state['signup_success'] = True
                else:
                    st.error(f"Error creating account: {message}")
    
    # Show login button outside the form if signup was successful
    if st.session_state.get('signup_success', False):
        if st.button("Go to Login Page", use_container_width=True):
            st.session_state['signup_success'] = False  # Reset the flag
            st.switch_page("streamlit_app.py")
    
    st.markdown("---")
    st.markdown("Already have an account?")
    if st.button("Back to Login", use_container_width=True):
        st.switch_page("streamlit_app.py")

def show_password_requirements():
    """Show password requirements"""
    with st.expander("Password Requirements"):
        st.write("""
        Your password must contain:
        - At least 8 characters
        - At least one uppercase letter (A-Z)
        - At least one lowercase letter (a-z)
        - At least one number (0-9)
        """)

if __name__ == "__main__":
    signup_page()
    show_password_requirements()
