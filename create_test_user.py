# create_test_user.py
from components.db import create_user, init_db

def create_test_user():
    # Initialize database first
    init_db()
    
    # Create a test user
    username = "testuser"
    email = "okarnkark06@gmail.com"  # Assuming gmail
    password = "TestPassword123"
    full_name = "Test User"
    
    success, message = create_user(username, email, password, full_name)
    
    if success:
        print(f"✅ Test user created successfully!")
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"Message: {message}")
    else:
        print(f"❌ Error creating user: {message}")

if __name__ == "__main__":
    create_test_user()
