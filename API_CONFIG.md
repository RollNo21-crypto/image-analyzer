# API Configuration Guide

## Getting Your Google Gemini API Key

### Step 1: Visit Google AI Studio

1. Open your web browser
2. Navigate to [Google AI Studio](https://makersuite.google.com/app/apikey)
3. Sign in with your Google account

### Step 2: Create API Key

1. Click "Create API Key" button
2. Choose your project (or create a new one)
3. The API key will be generated automatically
4. **Copy the API key immediately** - you won't be able to see it again

### Step 3: Configure Your Application

1. In your project folder, create a file named `.env`
2. Add the following line:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
3. Replace `your_api_key_here` with your actual API key
4. Save the file

### Example .env File

```env
# Google Gemini API Configuration
GEMINI_API_KEY=AIzaSyC1234567890abcdefghijklmnopqrstuvwxyz

# Optional: Other configurations
# DEBUG=True
# MAX_UPLOAD_SIZE=200
```

## API Key Security

### ⚠️ Important Security Notes

1. **Never share your API key publicly**
2. **Don't commit .env files to version control**
3. **Keep your API key confidential**
4. **Regenerate if compromised**

### .gitignore Configuration

Make sure your `.gitignore` file includes:
```gitignore
# Environment variables
.env
.env.local
.env.*.local

# Database
*.db

# Uploads
uploads/

# Python
__pycache__/
*.pyc
venv/
```

## API Usage & Limits

### Free Tier Limits

Google Gemini offers generous free tier limits:
- **Rate Limits**: 60 requests per minute
- **Daily Quota**: 1,500 requests per day
- **File Size**: Up to 20MB per image
- **Request Timeout**: 60 seconds

### Monitoring Usage

1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to "APIs & Services" → "Quotas"
3. Monitor your API usage and limits

### Upgrading Limits

If you need higher limits:
1. Visit Google Cloud Console
2. Enable billing on your project
3. Request quota increases if needed

## Testing Your API Key

### Method 1: Using the Application

1. Start your application: `streamlit run streamlit_app.py`
2. Click "🔧 Test API Connection" in the sidebar
3. You should see "✅ API Working: API connection successful"

### Method 2: Command Line Test

```bash
# Activate your virtual environment first
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Run the test
python -c "from components.gemini_client import test_api_connection; print(test_api_connection())"
```

### Method 3: Python Script Test

Create a test file `test_api.py`:

```python
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print(f"✅ API Key found: {api_key[:20]}...")
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    
    # Test the connection
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Hello, can you respond with 'API test successful'?")
        print(f"✅ API Response: {response.text}")
    except Exception as e:
        print(f"❌ API Error: {e}")
else:
    print("❌ API Key not found. Check your .env file.")
```

Run the test:
```bash
python test_api.py
```

## Troubleshooting API Issues

### Error: "GEMINI_API_KEY not found"

**Possible Causes:**
1. `.env` file doesn't exist
2. API key not properly formatted in `.env`
3. `.env` file in wrong location

**Solutions:**
1. Create `.env` file in project root directory
2. Check the format: `GEMINI_API_KEY=your_key_here`
3. Restart the application after creating/modifying `.env`

### Error: "API connection failed"

**Possible Causes:**
1. Invalid API key
2. No internet connection
3. API quota exceeded
4. API key expired or revoked

**Solutions:**
1. Generate a new API key
2. Check internet connection
3. Monitor usage in Google Cloud Console
4. Verify API key hasn't expired

### Error: "Rate limit exceeded"

**Cause:** Too many API requests in a short time

**Solutions:**
1. Wait a few minutes before trying again
2. Reduce the frequency of AI analysis
3. Consider upgrading to paid tier for higher limits

### Error: "Permission denied"

**Cause:** API key doesn't have proper permissions

**Solutions:**
1. Regenerate API key
2. Ensure Gemini API is enabled in your project
3. Check billing is set up (if required)

## Alternative AI Providers

If you prefer not to use Google Gemini, the application can be modified to work with:

### OpenAI GPT-4 Vision
```env
OPENAI_API_KEY=your_openai_key_here
```

### Anthropic Claude
```env
ANTHROPIC_API_KEY=your_anthropic_key_here
```

### Local AI Models
- Ollama with Vision models
- Hugging Face Transformers
- Custom vision models

*Note: Code modifications required for alternative providers*

## Environment Variables Reference

### Required Variables

```env
# Google Gemini API Key (required for AI features)
GEMINI_API_KEY=your_api_key_here
```

### Optional Variables

```env
# Debug mode (shows detailed error messages)
DEBUG=true

# Maximum upload file size in MB
MAX_UPLOAD_SIZE=200

# Database path (default: data.db)
DATABASE_PATH=data.db

# Upload directory (default: uploads/)
UPLOAD_DIR=uploads

# Application port (default: 8501)
PORT=8501

# Enable/disable AI features
ENABLE_AI=true
```

## Production Deployment

### Environment Setup

For production deployment:

1. **Use Environment Variables** instead of `.env` files
2. **Set up proper secrets management**
3. **Configure appropriate rate limiting**
4. **Monitor API usage and costs**

### Example Production Config

```bash
# Set environment variables in your deployment platform
export GEMINI_API_KEY="your_production_api_key"
export DEBUG="false"
export MAX_UPLOAD_SIZE="100"
```

### Docker Environment

If using Docker:

```dockerfile
# In your Dockerfile
ENV GEMINI_API_KEY=""
ENV DEBUG="false"

# Or use docker-compose.yml
services:
  app:
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - DEBUG=false
```

---

**Your API is now configured and ready to use! 🚀**
