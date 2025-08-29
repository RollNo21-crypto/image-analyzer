# components/db.py
import sqlite3
import bcrypt
import hashlib
from pathlib import Path
from datetime import datetime
import os

DB_PATH = "data.db"

def init_db():
    """Initialize the database with all required tables"""
    # Check if database already exists and has the users table
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            if c.fetchone():
                conn.close()
                return  # Database already initialized
            conn.close()
        except:
            pass  # Continue with initialization if check fails
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Create entries table with enhanced fields
    c.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            title TEXT,
            filename TEXT,
            description TEXT,
            image_caption TEXT,
            link TEXT,
            link_summary TEXT,
            categories TEXT,
            tags TEXT,
            file_path TEXT,
            file_size INTEGER,
            image_width INTEGER,
            image_height INTEGER,
            notes TEXT,
            is_favorite BOOLEAN DEFAULT 0,
            is_archived BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create sessions table for better session management
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_token TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def hash_password(password):
    """Hash a password for storing"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_user(username, email, password, full_name=None):
    """Create a new user"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Check if username or email already exists
        c.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
        if c.fetchone():
            conn.close()
            return False, "Username or email already exists"
        
        # Hash the password
        password_hash = hash_password(password)
        
        # Insert new user
        c.execute('''
            INSERT INTO users (username, email, password_hash, full_name)
            VALUES (?, ?, ?, ?)
        ''', (username, email, password_hash, full_name))
        
        conn.commit()
        user_id = c.lastrowid
        conn.close()
        
        return True, f"User created successfully with ID: {user_id}"
    
    except Exception as e:
        return False, f"Error creating user: {str(e)}"

def authenticate_user(username, password):
    """Authenticate a user"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute('SELECT id, password_hash, is_active FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        
        if not user:
            conn.close()
            return False, "User not found"
        
        user_id, password_hash, is_active = user
        
        if not is_active:
            conn.close()
            return False, "Account is deactivated"
        
        if verify_password(password, password_hash):
            # Update last login
            c.execute('UPDATE users SET last_login = ? WHERE id = ?', 
                     (datetime.now(), user_id))
            conn.commit()
            conn.close()
            return True, user_id
        else:
            conn.close()
            return False, "Invalid password"
    
    except Exception as e:
        return False, f"Authentication error: {str(e)}"

def get_user_by_username(username):
    """Get user details by username"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT id, username, email, full_name, created_at, last_login, is_active
        FROM users WHERE username = ?
    ''', (username,))
    user = c.fetchone()
    conn.close()
    return user

def save_entry(image_file, description, caption, link, summary, categories):
    """Legacy function for backward compatibility"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    filename = image_file.name
    c.execute('''
        INSERT INTO entries (username, filename, description, image_caption, link, link_summary, categories)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', ("legacy_user", filename, description, caption, link, summary, ",".join(categories)))
    conn.commit()
    conn.close()

def insert_data(username, image_file, description="", link="", summary="", categories="", 
                title="", tags="", notes="", is_favorite=False, **kwargs):
    """Insert data into the database with enhanced fields"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Get user ID
        user = get_user_by_username(username)
        if not user:
            return False, "User not found"
        
        user_id = user[0]
        filename = image_file.name if image_file else ""
        
        # Save file if it exists and get image dimensions
        file_path = None
        file_size = None
        image_width = None
        image_height = None
        
        if image_file:
            upload_dir = "uploads"
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}")
            
            with open(file_path, "wb") as f:
                f.write(image_file.getbuffer())
            file_size = len(image_file.getbuffer())
            
            # Get image dimensions
            try:
                from PIL import Image
                with Image.open(file_path) as img:
                    image_width, image_height = img.size
            except:
                pass  # If we can't get dimensions, just continue
        
        # Use filename as title if no title provided
        if not title:
            title = filename.rsplit('.', 1)[0] if filename else "Untitled"
        
        # Ensure categories and tags are strings
        if isinstance(categories, list):
            categories = ', '.join(categories)
        if isinstance(tags, list):
            tags = ', '.join(tags)
        
        # Insert the entry
        c.execute('''
            INSERT INTO entries (
                user_id, username, title, filename, description, image_caption,
                link, link_summary, categories, tags, file_path, file_size,
                image_width, image_height, notes, is_favorite, is_archived
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id, username, title, filename, description, summary,
            link, "", categories, tags, file_path, file_size,
            image_width, image_height, notes, is_favorite, False
        ))
        
        conn.commit()
        conn.close()
        return True, "Entry saved successfully"
        
    except Exception as e:
        return False, f"Error saving entry: {str(e)}"
def get_entries(username=None, user_id=None, limit=None):
    """Retrieve entries from the database, optionally filtered by username or user_id"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    query = '''
        SELECT id, username, filename, description, image_caption, 
               link, link_summary, categories, uploaded_at, user_id, 
               file_path, file_size, title, tags, image_width, 
               image_height, notes, is_favorite, is_archived
        FROM entries
    '''
    params = []
    
    if username:
        query += ' WHERE username = ?'
        params.append(username)
    elif user_id:
        query += ' WHERE user_id = ?'
        params.append(user_id)
    
    query += ' ORDER BY uploaded_at DESC'
    
    if limit:
        query += ' LIMIT ?'
        params.append(limit)
    
    c.execute(query, params)
    entries = c.fetchall()
    conn.close()
    return entries

def get_user_stats(username):
    """Get statistics for a user"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get total entries
    c.execute('SELECT COUNT(*) FROM entries WHERE username = ?', (username,))
    total_entries = c.fetchone()[0]
    
    # Get total file size
    c.execute('SELECT SUM(file_size) FROM entries WHERE username = ? AND file_size IS NOT NULL', (username,))
    total_size = c.fetchone()[0] or 0
    
    # Get most recent upload
    c.execute('SELECT MAX(uploaded_at) FROM entries WHERE username = ?', (username,))
    last_upload = c.fetchone()[0]
    
    conn.close()
    
    return {
        'total_entries': total_entries,
        'total_size_mb': round(total_size / (1024 * 1024), 2) if total_size else 0,
        'last_upload': last_upload
    }

def update_entry(entry_id, update_data, user_id=None):
    """Update an entry with new data"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Verify the entry exists (and belongs to user if user_id provided)
        if user_id:
            c.execute('SELECT id FROM entries WHERE id = ? AND user_id = ?', (entry_id, user_id))
        else:
            c.execute('SELECT id FROM entries WHERE id = ?', (entry_id,))
            
        if not c.fetchone():
            conn.close()
            return False
        
        # Build update query dynamically
        allowed_fields = [
            'title', 'description', 'image_caption', 'link', 'link_summary', 
            'categories', 'tags', 'notes', 'is_favorite', 'is_archived'
        ]
        
        update_fields = []
        params = []
        
        for field, value in update_data.items():
            if field in allowed_fields:
                update_fields.append(f"{field} = ?")
                params.append(value)
        
        if not update_fields:
            conn.close()
            return False
        
        # Add updated_at timestamp
        update_fields.append("updated_at = ?")
        params.append(datetime.now().isoformat())
        params.append(entry_id)
        
        query = f"UPDATE entries SET {', '.join(update_fields)} WHERE id = ?"
        c.execute(query, params)
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        return False

def delete_entry(entry_id, user_id=None):
    """Delete an entry and its associated file"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Get entry info before deletion
        if user_id:
            c.execute('SELECT file_path FROM entries WHERE id = ? AND user_id = ?', (entry_id, user_id))
        else:
            c.execute('SELECT file_path FROM entries WHERE id = ?', (entry_id,))
            
        entry = c.fetchone()
        
        if not entry:
            conn.close()
            return False
        
        file_path = entry[0]
        
        # Delete the entry from database
        if user_id:
            c.execute('DELETE FROM entries WHERE id = ? AND user_id = ?', (entry_id, user_id))
        else:
            c.execute('DELETE FROM entries WHERE id = ?', (entry_id,))
        
        # Delete the physical file if it exists
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass  # Continue even if file deletion fails
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        return False

def get_entry_by_id(entry_id, user_id=None):
    """Get a specific entry by ID"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if user_id:
        c.execute('''
            SELECT id, username, filename, description, image_caption, 
                   link, link_summary, categories, uploaded_at, user_id, 
                   file_path, file_size, title, tags, image_width, 
                   image_height, notes, is_favorite, is_archived
            FROM entries 
            WHERE id = ? AND user_id = ?
        ''', (entry_id, user_id))
    else:
        c.execute('''
            SELECT id, username, filename, description, image_caption, 
                   link, link_summary, categories, uploaded_at, user_id, 
                   file_path, file_size, title, tags, image_width, 
                   image_height, notes, is_favorite, is_archived
            FROM entries 
            WHERE id = ?
        ''', (entry_id,))
    
    entry = c.fetchone()
    conn.close()
    return entry

def search_entries(username, search_query="", category="", tag="", favorites_only=False, 
                  exclude_archived=False, **kwargs):
    """Search entries with various filters"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        query = '''
            SELECT id, username, filename, description, image_caption, 
                   link, link_summary, categories, uploaded_at, user_id, 
                   file_path, file_size, title, tags, image_width, 
                   image_height, notes, is_favorite, is_archived
            FROM entries 
            WHERE username = ?
        '''
        params = [username]
        
        # Add search filters
        if search_query:
            query += ''' AND (
                title LIKE ? OR description LIKE ? OR image_caption LIKE ? 
                OR filename LIKE ? OR tags LIKE ? OR notes LIKE ?
            )'''
            search_pattern = f"%{search_query}%"
            params.extend([search_pattern] * 6)
        
        if category:
            query += ' AND categories LIKE ?'
            params.append(f"%{category}%")
        
        if tag:
            query += ' AND tags LIKE ?'
            params.append(f"%{tag}%")
        
        if favorites_only:
            query += ' AND is_favorite = 1'
        
        if exclude_archived:
            query += ' AND (is_archived = 0 OR is_archived IS NULL)'
        
        query += ' ORDER BY uploaded_at DESC'
        
        c.execute(query, params)
        entries = c.fetchall()
        conn.close()
        return entries
        
    except Exception as e:
        return []

def get_all_categories(username):
    """Get all unique categories for a user"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('SELECT DISTINCT categories FROM entries WHERE username = ? AND categories IS NOT NULL', (username,))
    rows = c.fetchall()
    conn.close()
    
    categories = set()
    for row in rows:
        if row[0]:
            for cat in row[0].split(','):
                categories.add(cat.strip())
    
    return sorted(list(categories))

def get_all_tags(username):
    """Get all unique tags for a user"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('SELECT DISTINCT tags FROM entries WHERE username = ? AND tags IS NOT NULL', (username,))
    rows = c.fetchall()
    conn.close()
    
    tags = set()
    for row in rows:
        if row[0]:
            for tag in row[0].split(','):
                tags.add(tag.strip())
    
    return sorted(list(tags))
