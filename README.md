# 🖼️ Image Knowledge Base - Setup Guide

A comprehensive AI-powered image management and analysis system built with Streamlit and Google Gemini.

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)

## ✨ Features

- 🤖 **AI-Powered Image Analysis** - Automatic image description and categorization using Google Gemini
- 📊 **Visual Dashboard** - Overview of your collection with image galleries and statistics
- 🔍 **Advanced Search** - Search by content, categories, tags, and metadata
- ⭐ **Favorites System** - Mark and organize your favorite images
- 📝 **Full CRUD Operations** - Create, Read, Update, Delete entries
- 👤 **User Authentication** - Secure user accounts and session management
- 🏷️ **Tagging & Categories** - Organize images with custom tags and categories
- 💾 **Local Storage** - Images and metadata stored locally
- 📱 **Responsive Design** - Works on desktop and mobile devices

## 🔧 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** (recommended: Python 3.9 or higher)
- **Git** (for cloning the repository)
- **Google Gemini API Key** (for AI features)

### System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: At least 1GB free space
- **Internet Connection**: Required for AI analysis features

## 📦 Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd image-analyzer
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Additional Dependencies (if needed)

```bash
pip install --upgrade streamlit pillow python-dotenv bcrypt google-generativeai pandas
```

## ⚙️ Configuration

### Step 1: Create Environment File

Create a `.env` file in the project root directory:

```bash
# Create .env file
touch .env  # On macOS/Linux
# Or create manually on Windows
```

### Step 2: Add API Configuration

Add your Google Gemini API key to the `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

#### How to Get a Gemini API Key:

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key
5. Paste it in your `.env` file

### Step 3: Initialize Database

The database will be automatically initialized when you first run the application. No manual setup required!

## 🚀 Running the Application

### Step 1: Activate Virtual Environment

```bash
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Start the Application

```bash
streamlit run streamlit_app.py
```

### Step 3: Access the Application

The application will automatically open in your web browser at:
- **Local URL**: `http://localhost:8501`
- **Network URL**: `http://192.168.x.x:8501` (for network access)

## 📖 Usage Guide

### First Time Setup

1. **Open the Application** in your web browser
2. **Create an Account** by clicking on the signup option
3. **Log In** with your credentials
4. **Upload Your First Image** using the "Add Entry" page

### Main Features

#### 🖼️ Add Entry
- Upload images (JPG, PNG, GIF, BMP)
- Enable AI analysis for automatic descriptions
- Add custom titles, descriptions, and notes
- Organize with categories and tags
- Mark as favorites

#### 📊 Dashboard
- View collection statistics
- Browse recent images in gallery format
- Quick search functionality
- Access favorite entries

#### 🔍 Search & Browse
- Advanced filtering options
- Search by text, categories, or tags
- Sort by date, title, or file size
- Pagination for large collections

#### ⭐ Favorites
- View all favorite entries
- Quick unfavorite options
- Easy access to frequently used images

#### 📝 Manage Entries
- Edit entry details
- Update categories and tags
- Archive or delete entries
- Bulk operations

### Tips for Best Results

1. **Use Descriptive Titles** - Make your images easy to find
2. **Add Relevant Tags** - Use consistent tagging for better organization
3. **Enable AI Analysis** - Let Gemini automatically categorize your images
4. **Regular Cleanup** - Archive or delete unused entries
5. **Backup Important Images** - Keep copies of critical images

## 🔧 Troubleshooting

### Common Issues

#### Issue: "GEMINI_API_KEY not found"
**Solution:**
1. Check that your `.env` file exists in the project root
2. Verify the API key is correctly formatted
3. Restart the application after adding the key

#### Issue: Database errors
**Solution:**
1. Delete `data.db` file and restart the application
2. Run the migration script: `python migrate_schema.py`

#### Issue: Images not displaying
**Solution:**
1. Check that the `uploads` folder exists
2. Verify file permissions
3. Ensure images were uploaded successfully

#### Issue: Port already in use
**Solution:**
```bash
streamlit run streamlit_app.py --server.port 8502
```

#### Issue: Module not found errors
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Debug Mode

To run in debug mode for troubleshooting:

```bash
streamlit run streamlit_app.py --logger.level debug
```

### Reset Application

To completely reset the application:

1. Stop the application (`Ctrl+C`)
2. Delete `data.db` file
3. Delete `uploads` folder
4. Restart the application

## 📁 Project Structure

```
image-analyzer/
├── streamlit_app.py          # Main application file
├── requirements.txt          # Python dependencies
├── .env                     # Environment variables (create this)
├── README.md               # This file
├── data.db                 # SQLite database (auto-created)
├── uploads/                # Image storage folder (auto-created)
├── components/             # Application modules
│   ├── __init__.py
│   ├── auth.py            # Authentication system
│   ├── db.py              # Database operations
│   ├── gemini_client.py   # AI/Gemini integration
│   ├── image_processor.py # Image processing
│   └── text_extractor.py  # Text extraction
├── config/                # Configuration files
│   └── auth_config.yaml   # Auth configuration
├── pages/                 # Additional pages
│   └── dashboard.py       # Dashboard components
└── venv/                  # Virtual environment (auto-created)
```

## 🆘 Getting Help

If you encounter issues:

1. **Check the Console** - Look for error messages in the terminal
2. **Review the Logs** - Check Streamlit logs for detailed error information
3. **Restart the Application** - Many issues resolve with a restart
4. **Check Dependencies** - Ensure all packages are correctly installed
5. **Verify Configuration** - Double-check your `.env` file

## 🔄 Updates

To update the application:

```bash
# Pull latest changes (if using git)
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart the application
streamlit run streamlit_app.py
```

## 📝 Notes

- The application creates a local SQLite database (`data.db`)
- Images are stored in the `uploads/` directory
- User passwords are securely hashed using bcrypt
- AI features require an active internet connection
- The application is designed for personal/local use

---

**Enjoy your Image Knowledge Base! 🖼️✨**
