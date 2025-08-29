# test_api.py
import os
from dotenv import load_dotenv
from components.gemini_client import test_api_connection

def main():
    # Load environment variables
    load_dotenv()
    
    print("Testing Gemini API connection...")
    print(f"API Key: {os.getenv('GEMINI_API_KEY')[:10]}..." if os.getenv('GEMINI_API_KEY') else "No API key found")
    
    success, message = test_api_connection()
    
    if success:
        print("✅ API connection successful!")
        print(f"Response: {message}")
    else:
        print("❌ API connection failed!")
        print(f"Error: {message}")
        print("\nPossible solutions:")
        print("1. Check if your API key is correct")
        print("2. Verify the API key has the necessary permissions")
        print("3. Check if you've exceeded API quotas")
        print("4. Ensure you're using the correct Gemini API endpoint")

if __name__ == "__main__":
    main()
