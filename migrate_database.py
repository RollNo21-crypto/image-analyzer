# migrate_database.py
import sqlite3
import os
from components.db import init_db

def check_database_schema():
    """Check current database schema"""
    print("Checking current database schema...")
    
    if not os.path.exists('data.db'):
        print("Database doesn't exist. Creating new one...")
        init_db()
        return
    
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    # Check entries table structure
    cursor.execute('PRAGMA table_info(entries)')
    entries_columns = cursor.fetchall()
    print("\nCurrent 'entries' table structure:")
    for column in entries_columns:
        print(f"  {column}")
    
    # Check if users table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    users_exists = cursor.fetchone()
    
    if users_exists:
        cursor.execute('PRAGMA table_info(users)')
        users_columns = cursor.fetchall()
        print("\nCurrent 'users' table structure:")
        for column in users_columns:
            print(f"  {column}")
    else:
        print("\n'users' table doesn't exist")
    
    conn.close()

def migrate_database():
    """Migrate database to new schema"""
    print("\nMigrating database...")
    
    # Backup the old database
    if os.path.exists('data.db'):
        import shutil
        shutil.copy('data.db', 'data_backup.db')
        print("Created backup: data_backup.db")
    
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    try:
        # Check if users table exists, if not create it
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("Creating users table...")
            cursor.execute('''
                CREATE TABLE users (
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
        
        # Check and add missing columns to entries table
        cursor.execute('PRAGMA table_info(entries)')
        existing_columns = [column[1] for column in cursor.fetchall()]
        
        new_columns = [
            ('user_id', 'INTEGER'),
            ('file_path', 'TEXT'),
            ('file_size', 'INTEGER')
        ]
        
        for column_name, column_type in new_columns:
            if column_name not in existing_columns:
                print(f"Adding column {column_name} to entries table...")
                cursor.execute(f'ALTER TABLE entries ADD COLUMN {column_name} {column_type}')
        
        # Create user_sessions table if it doesn't exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_sessions'")
        if not cursor.fetchone():
            print("Creating user_sessions table...")
            cursor.execute('''
                CREATE TABLE user_sessions (
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
        print("Migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    check_database_schema()
    migrate_database()
    print("\nChecking schema after migration:")
    check_database_schema()
