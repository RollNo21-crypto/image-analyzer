# Installation Guide - Image Knowledge Base

## Quick Start (5 minutes)

### Prerequisites Check
```bash
# Check Python version (should be 3.8+)
python --version

# Check pip
pip --version
```

### Installation Steps

1. **Download/Clone the Project**
   ```bash
   # If you have the zip file, extract it
   # If using git:
   git clone <your-repo-url>
   cd image-analyzer
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   ```bash
   # Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   
   # Windows (Command Prompt):
   venv\Scripts\activate
   
   # macOS/Linux:
   source venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create Configuration File**
   Create a file named `.env` in the project folder:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

6. **Run the Application**
   ```bash
   streamlit run streamlit_app.py
   ```

7. **Open in Browser**
   - The app will automatically open at `http://localhost:8501`
   - Create an account and start uploading images!

## Detailed Installation

### For Windows Users

1. **Install Python** (if not already installed)
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **Open PowerShell or Command Prompt**
   - Press `Win + R`, type `powershell`, press Enter

3. **Navigate to Project Folder**
   ```powershell
   cd C:\path\to\your\image-analyzer
   ```

4. **Follow Quick Start Steps 2-7**

### For macOS Users

1. **Install Python** (if not already installed)
   ```bash
   # Using Homebrew (recommended)
   brew install python
   
   # Or download from python.org
   ```

2. **Open Terminal**
   - Press `Cmd + Space`, type "Terminal", press Enter

3. **Follow Quick Start Steps 1-7**

### For Linux Users

1. **Install Python** (if not already installed)
   ```bash
   # Ubuntu/Debian:
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   
   # CentOS/RHEL:
   sudo yum install python3 python3-pip
   ```

2. **Follow Quick Start Steps 1-7**

## Getting Your Gemini API Key

1. **Visit Google AI Studio**
   - Go to [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

2. **Sign In**
   - Use your Google account

3. **Create API Key**
   - Click "Create API Key"
   - Copy the generated key

4. **Add to .env File**
   ```env
   GEMINI_API_KEY=AIzaSyC...your-key-here
   ```

## Verification

After installation, verify everything works:

1. **Check Virtual Environment**
   ```bash
   # Should show (venv) in your prompt
   which python  # Should point to venv folder
   ```

2. **Test Dependencies**
   ```bash
   python -c "import streamlit; print('Streamlit OK')"
   python -c "import PIL; print('PIL OK')"
   python -c "import google.generativeai; print('Gemini OK')"
   ```

3. **Run Application**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Test in Browser**
   - Should open automatically
   - Try creating an account
   - Upload a test image

## Common Installation Issues

### Issue: "Python not found"
**Solution:**
- Install Python from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation

### Issue: "pip not found"
**Solution:**
```bash
# Windows:
python -m ensurepip --upgrade

# macOS/Linux:
sudo apt install python3-pip  # Ubuntu/Debian
```

### Issue: "Permission denied"
**Solution:**
```bash
# Don't use sudo with pip in virtual environment
# Make sure virtual environment is activated
```

### Issue: "Virtual environment not working"
**Solution:**
```bash
# Delete and recreate
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows

python -m venv venv
```

### Issue: "Module not found after installation"
**Solution:**
```bash
# Make sure virtual environment is activated
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

## Performance Optimization

### For Large Image Collections

1. **Increase Memory** (if needed)
   ```bash
   streamlit run streamlit_app.py --server.maxUploadSize 200
   ```

2. **Database Optimization**
   - The app automatically optimizes the SQLite database
   - For very large collections (>10,000 images), consider periodic cleanup

### For Slow AI Analysis

1. **Check Internet Connection**
   - AI features require internet access

2. **Use Smaller Images**
   - Resize images before upload for faster processing

## Development Setup

If you want to modify the code:

1. **Install Development Dependencies**
   ```bash
   pip install pytest black flake8 mypy
   ```

2. **Run Tests**
   ```bash
   pytest tests/  # If test folder exists
   ```

3. **Code Formatting**
   ```bash
   black *.py
   flake8 *.py
   ```

## Backup and Migration

### Backup Your Data

1. **Backup Database**
   ```bash
   cp data.db data_backup.db
   ```

2. **Backup Images**
   ```bash
   cp -r uploads uploads_backup
   ```

### Restore Data

1. **Restore Database**
   ```bash
   cp data_backup.db data.db
   ```

2. **Restore Images**
   ```bash
   cp -r uploads_backup uploads
   ```

## Uninstallation

To completely remove the application:

1. **Deactivate Virtual Environment**
   ```bash
   deactivate
   ```

2. **Delete Project Folder**
   ```bash
   rm -rf image-analyzer  # Linux/macOS
   rmdir /s image-analyzer  # Windows
   ```

---

**Need help? Check the main README.md for troubleshooting tips!**
