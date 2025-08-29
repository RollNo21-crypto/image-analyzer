#!/usr/bin/env python3
"""Fix deprecated Streamlit parameters"""

# Read the file with UTF-8 encoding
with open('streamlit_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace deprecated parameters
content = content.replace('use_column_width=False', 'use_container_width=False')
content = content.replace('use_column_width=True', 'use_container_width=True')

# Write back with UTF-8 encoding
with open('streamlit_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed all deprecated use_column_width parameters")
