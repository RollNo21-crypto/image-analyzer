# debug_entries.py
from components.db import get_entries

def debug_entries():
    """Debug the entries structure"""
    print("Debugging entries structure...")
    
    entries = get_entries(limit=3)
    
    if entries:
        print(f"\nFound {len(entries)} entries")
        for i, entry in enumerate(entries):
            print(f"\nEntry {i}:")
            print(f"  Length: {len(entry)}")
            print(f"  Data: {entry}")
            
            # Print each field with its index
            field_names = [
                'id', 'username', 'filename', 'description', 'image_caption',
                'link', 'link_summary', 'categories', 'uploaded_at', 'file_path', 'file_size'
            ]
            
            for idx, field_name in enumerate(field_names):
                if idx < len(entry):
                    print(f"  [{idx}] {field_name}: {entry[idx]}")
                else:
                    print(f"  [{idx}] {field_name}: MISSING")
    else:
        print("No entries found")

if __name__ == "__main__":
    debug_entries()
