# components/gemini_client.py

import os
import google.generativeai as genai
from PIL import Image
import io
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini with API key
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("Warning: GEMINI_API_KEY not found. Using mock responses.")
    API_KEY = None
else:
    print(f"✅ GEMINI_API_KEY loaded successfully")

if API_KEY:
    genai.configure(api_key=API_KEY)
    # Use the best available models
    vision_model = genai.GenerativeModel("gemini-1.5-flash")  # Good for image analysis
    text_model = genai.GenerativeModel("gemini-1.5-flash")    # Good for text generation
else:
    vision_model = None
    text_model = None

def analyze_image_with_gemini(image_data, prompt: str) -> str:
    """Analyze an image using Gemini Vision API"""
    if not API_KEY or not vision_model:
        return "Mock analysis: This appears to be an interesting image. The AI analysis is currently unavailable because the GEMINI_API_KEY is not configured."
    
    try:
        # Convert image data to PIL Image
        if hasattr(image_data, 'read'):
            image_bytes = image_data.read()
            image_data.seek(0)  # Reset pointer
        else:
            image_bytes = image_data
        
        image = Image.open(io.BytesIO(image_bytes))
        
        # Generate content with image and prompt
        response = vision_model.generate_content([prompt, image])
        return response.text.strip()
        
    except Exception as e:
        return f"⚠️ Gemini Vision analysis failed: {str(e)}"

def summarize_with_gemini(text: str) -> str:
    """Summarize text using Gemini"""
    if not API_KEY or not text_model:
        return "Mock summary: This text discusses various topics. The AI summarization is currently unavailable because the GEMINI_API_KEY is not configured."
    
    try:
        response = text_model.generate_content(text)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Gemini text summarization failed: {str(e)}"

def list_available_models():
    """List all available Gemini models"""
    if not API_KEY:
        return ["No API key available"]
    
    try:
        models = genai.list_models()
        return [model.name for model in models]
    except Exception as e:
        return f"Error listing models: {str(e)}"

def test_api_connection():
    """Test if the API key is working"""
    if not API_KEY:
        return False, "GEMINI_API_KEY not found in environment variables. Please check your .env file."
    
    try:
        # First, let's try to list models to see what's available
        print("Available models:", list_available_models())
        
        response = text_model.generate_content("Hello, can you respond with 'API connection successful'?")
        return True, response.text.strip()
    except Exception as e:
        return False, str(e)
