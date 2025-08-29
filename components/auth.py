# components/auth.py
import streamlit as st
from components.db import authenticate_user, get_user_by_username

def login_form():
    """Display login form"""
    st.title("🔐 Login to Image Analyzer")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login", use_container_width=True)
        
        if login_button:
            if username and password:
                success, result = authenticate_user(username, password)
                
                if success:
                    user = get_user_by_username(username)
                    st.session_state['authentication_status'] = True
                    st.session_state['username'] = username
                    st.session_state['name'] = user[3] if user[3] else username  # full_name or username
                    st.session_state['user_id'] = result  # user_id returned from authenticate_user
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(f"Login failed: {result}")
            else:
                st.error("Please enter both username and password")
    
    st.markdown("---")
    st.markdown("Don't have an account?")
    if st.button("Sign Up", use_container_width=True):
        st.switch_page("pages/signup.py")

def logout():
    """Handle logout"""
    st.session_state['authentication_status'] = False
    st.session_state['username'] = None
    st.session_state['name'] = None
    st.session_state['user_id'] = None
    st.success("Logged out successfully!")
    st.rerun()

def check_authentication():
    """Check if user is authenticated"""
    return st.session_state.get('authentication_status', False)

def get_current_user():
    """Get current user info"""
    return {
        'username': st.session_state.get('username'),
        'name': st.session_state.get('name'),
        'user_id': st.session_state.get('user_id')
    }
