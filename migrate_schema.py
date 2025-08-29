#!/usr/bin/env python3
"""
Database schema migration script to add missing columns to the entries table
"""

import sqlite3
import os

DB_PATH = "data.db"

def migrate_database():
    """Add missing columns to the entries table"""
    print("Starting database migration...")
    
    if not os.path.exists(DB_PATH):
        print("Database doesn't exist. Please run the app first to create it.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get current schema
    c.execute("PRAGMA table_info(entries)")
    current_columns = [row[1] for row in c.fetchall()]
    print(f"Current columns: {current_columns}")
    
    # List of columns that should exist
    required_columns = [
        ('title', 'TEXT'),
        ('tags', 'TEXT'),
        ('image_width', 'INTEGER'),
        ('image_height', 'INTEGER'),
        ('notes', 'TEXT'),
        ('is_favorite', 'BOOLEAN DEFAULT 0'),
        ('is_archived', 'BOOLEAN DEFAULT 0'),
        ('created_at', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'),
        ('updated_at', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
    ]
    
    # Add missing columns
    for column_name, column_type in required_columns:
        if column_name not in current_columns:
            try:
                c.execute(f"ALTER TABLE entries ADD COLUMN {column_name} {column_type}")
                print(f"✅ Added column: {column_name}")
            except Exception as e:
                print(f"❌ Error adding column {column_name}: {e}")
    
    # Update the field mapping to match current database
    c.execute("PRAGMA table_info(entries)")
    final_columns = [row[1] for row in c.fetchall()]
    print(f"Final columns: {final_columns}")
    
    conn.commit()
    conn.close()
    print("Migration completed!")

if __name__ == "__main__":
    migrate_database()
