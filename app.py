import streamlit as st
import os
import pandas as pd
from datetime import datetime
from PIL import Image
import json
from components.image_processor import analyze_image
from components.db import (
    init_db, insert_data, get_user_stats, get_entries,
    search_entries, get_entry_by_id, update_entry, delete_entry,
    get_all_categories, get_all_tags
)
from components.auth import login_form, logout, check_authentication, get_current_user

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Helper functions for entry field access
def get_entry_field(entry, field_name):
    """Safely get a field from an entry tuple"""
    field_mapping = {
        'id': 0, 'user_id': 1, 'username': 2, 'title': 3, 'filename': 4,
        'description': 5, 'image_caption': 6, 'link': 7, 'link_summary': 8,
        'categories': 9, 'tags': 10, 'file_path': 11, 'file_size': 12,
        'image_width': 13, 'image_height': 14, 'notes': 15, 'is_favorite': 16,
        'is_archived': 17, 'created_at': 18, 'updated_at': 19, 'uploaded_at': 20
    }
    
    if field_name not in field_mapping:
        return None
    
    index = field_mapping[field_name]
    if len(entry) > index:
        return entry[index]
    return None

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if not size_bytes:
        return "Unknown"
    
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{round(size_bytes/1024, 2)} KB"
    else:
        return f"{round(size_bytes/(1024*1024), 2)} MB"

def parse_tags_categories(text):
    """Parse comma-separated tags/categories"""
    if not text:
        return []
    return [item.strip() for item in text.split(',') if item.strip()]

def display_image_card(entry, show_edit_controls=False):
    """Display an image entry as a card"""
    entry_id = get_entry_field(entry, 'id')
    filename = get_entry_field(entry, 'filename') or 'Unknown'
    title = get_entry_field(entry, 'title') or filename
    description = get_entry_field(entry, 'description') or ''
    file_path = get_entry_field(entry, 'file_path')
    is_favorite = get_entry_field(entry, 'is_favorite')
    is_archived = get_entry_field(entry, 'is_archived')
    tags = get_entry_field(entry, 'tags') or ''
    categories = get_entry_field(entry, 'categories') or ''
    created_at = get_entry_field(entry, 'created_at')
    file_size = get_entry_field(entry, 'file_size')
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            # Display image if file exists
            if file_path and os.path.exists(file_path):
                try:
                    st.image(file_path, width=150, caption=filename)
                except:
                    st.write("🖼️ Image unavailable")
            else:
                st.write("🖼️ Image not found")
        
        with col2:
            # Title and description
            title_text = f"{'⭐' if is_favorite else ''}{'📦' if is_archived else ''} {title}"
            st.write(f"**{title_text}**")
            
            if description:
                st.write(description[:200] + "..." if len(description) > 200 else description)
            
            # Tags and categories
            if tags:
                st.write(f"🏷️ **Tags:** {tags}")
            if categories:
                st.write(f"📁 **Categories:** {categories}")
            
            # Metadata
            if created_at:
                st.caption(f"📅 Created: {created_at[:16]}")
            if file_size:
                st.caption(f"💾 Size: {format_file_size(file_size)}")
        
        with col3:
            if show_edit_controls:
                if st.button(f"✏️ Edit", key=f"edit_{entry_id}"):
                    st.session_state[f'edit_entry_{entry_id}'] = True
                    st.rerun()
                
                if st.button(f"❤️ {'Unfav' if is_favorite else 'Fav'}", key=f"fav_{entry_id}"):
                    update_entry(entry_id, {'is_favorite': not is_favorite})
                    st.rerun()
                
                if st.button(f"🗑️ Delete", key=f"del_{entry_id}"):
                    if st.session_state.get(f'confirm_delete_{entry_id}'):
                        delete_entry(entry_id)
                        st.success("Entry deleted!")
                        st.rerun()
                    else:
                        st.session_state[f'confirm_delete_{entry_id}'] = True
                        st.warning("Click again to confirm deletion")
        
        st.divider()

# Initialize database
init_db()

# Configure page
st.set_page_config(
    page_title="Image Knowledge Base",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = False

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Authentication check
if not check_authentication():
    st.title("🖼️ Image Knowledge Base")
    st.write("A comprehensive tool for managing and analyzing your image collection with AI-powered insights.")
    login_form()
else:
    # User is authenticated, show the main app
    current_user = get_current_user()
    username = current_user['username']
    name = current_user['name']
    
    # Sidebar with user info and navigation
    with st.sidebar:
        st.success(f"Welcome, {name}! 👋")
        
        # User stats
        stats = get_user_stats(username)
        st.metric("Total Entries", stats['total_entries'])
        st.metric("Storage Used", f"{stats['total_size_mb']} MB")
        
        # Quick stats
        user_entries = get_entries(username=username)
        favorites_count = sum(1 for entry in user_entries if get_entry_field(entry, 'is_favorite'))
        archived_count = sum(1 for entry in user_entries if get_entry_field(entry, 'is_archived'))
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Favorites", favorites_count)
        with col2:
            st.metric("Archived", archived_count)
        
        st.markdown("---")
        
        # Navigation
        pages = [
            "🏠 Dashboard",
            "➕ Add Entry", 
            "🔍 Search & Browse",
            "⭐ Favorites",
            "✏️ Manage Entries",
            "📊 Categories & Tags"
        ]
        page = st.selectbox("Navigate", pages)
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout()

    # Main content area
    if page == "🏠 Dashboard":
        st.title("📊 Dashboard")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Entries", stats['total_entries'])
        with col2:
            st.metric("Storage Used", f"{stats['total_size_mb']} MB")
        with col3:
            st.metric("Favorites", favorites_count)
        with col4:
            st.metric("Archived", archived_count)
        
        st.markdown("---")
        
        # Recent activity
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📈 Recent Entries")
            recent_entries = get_entries(username=username, limit=5)
            
            if recent_entries:
                for entry in recent_entries:
                    display_image_card(entry)
            else:
                st.info("No entries yet. Start by adding your first image!")
        
        with col2:
            st.subheader("🏷️ Top Categories")
            all_categories = get_all_categories(username)
            if all_categories:
                for category, count in all_categories[:10]:
                    st.write(f"📁 {category}: {count}")
            else:
                st.info("No categories yet")
            
            st.subheader("📋 Quick Actions")
            if st.button("➕ Add New Entry", use_container_width=True):
                st.session_state.page = "➕ Add Entry"
                st.rerun()
            if st.button("🔍 Search Entries", use_container_width=True):
                st.session_state.page = "🔍 Search & Browse"
                st.rerun()

    elif page == "➕ Add Entry":
        st.title("➕ Add New Entry")
        
        with st.form("add_entry_form"):
            col1, col2 = st.columns([1, 1])
            
            with col1:
                # Image upload
                uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png", "gif", "bmp"])
                
                if uploaded_file:
                    st.image(uploaded_file, caption="Preview", use_column_width=True)
                
                # AI Analysis
                use_ai = st.checkbox("Use AI for automatic analysis", value=True)
                
            with col2:
                # Entry details
                title = st.text_input("Title (optional)")
                description = st.text_area("Description", height=100)
                
                # Categories and tags
                categories = st.text_input("Categories (comma-separated)", 
                                         help="e.g., nature, landscape, travel")
                tags = st.text_input("Tags (comma-separated)", 
                                    help="e.g., sunset, mountains, vacation")
                
                # Additional metadata
                link = st.text_input("Related Link (optional)")
                notes = st.text_area("Notes (optional)", height=80)
                
                # Options
                is_favorite = st.checkbox("Mark as favorite")
            
            submitted = st.form_submit_button("🚀 Add Entry", use_container_width=True)
            
            if submitted and uploaded_file:
                with st.spinner("Processing and analyzing image..."):
                    try:
                        # Use AI analysis if enabled
                        ai_result = None
                        if use_ai:
                            ai_result = analyze_image(uploaded_file, description, link)
                        
                        # Prepare data
                        entry_data = {
                            'title': title or uploaded_file.name,
                            'description': description,
                            'categories': categories,
                            'tags': tags,
                            'link': link,
                            'notes': notes,
                            'is_favorite': is_favorite
                        }
                        
                        # If AI analysis was successful, merge results
                        if ai_result:
                            if not description and ai_result.get('summary'):
                                entry_data['description'] = ai_result['summary']
                            if not categories and ai_result.get('categories'):
                                entry_data['categories'] = ', '.join(ai_result['categories'])
                        
                        # Insert into database
                        success, message = insert_data(
                            username=username,
                            image_file=uploaded_file,
                            **entry_data
                        )
                        
                        if success:
                            st.success("✅ Entry added successfully!")
                            if ai_result:
                                st.info("🤖 AI analysis completed and integrated")
                        else:
                            st.error(f"❌ Error: {message}")
                    
                    except Exception as e:
                        st.error(f"Error processing entry: {str(e)}")
            
            elif submitted:
                st.warning("Please upload an image first")

    elif page == "🔍 Search & Browse":
        st.title("🔍 Search & Browse")
        
        # Search and filter controls
        with st.expander("🔧 Search & Filter Options", expanded=True):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                search_query = st.text_input("🔍 Search in titles, descriptions, notes...", 
                                           placeholder="Enter search terms")
            
            with col2:
                category_filter = st.selectbox("📁 Category", 
                                             ["All"] + [cat[0] for cat in get_all_categories(username)])
            
            with col3:
                tag_filter = st.selectbox("🏷️ Tag", 
                                        ["All"] + [tag[0] for tag in get_all_tags(username)])
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                show_favorites = st.checkbox("⭐ Favorites only")
            with col2:
                show_archived = st.checkbox("📦 Show archived")
            with col3:
                sort_by = st.selectbox("Sort by", ["Recent", "Title", "Size"])
            with col4:
                entries_per_page = st.selectbox("Per page", [12, 24, 48])
        
        # Build search parameters
        search_params = {}
        if search_query:
            search_params['search_query'] = search_query
        if category_filter != "All":
            search_params['category'] = category_filter
        if tag_filter != "All":
            search_params['tag'] = tag_filter
        if show_favorites:
            search_params['favorites_only'] = True
        if not show_archived:
            search_params['exclude_archived'] = True
        
        # Get search results
        if search_params:
            entries = search_entries(username, **search_params)
        else:
            entries = get_entries(username=username)
        
        # Filter archived entries if needed
        if not show_archived:
            entries = [e for e in entries if not get_entry_field(e, 'is_archived')]
        
        # Sort entries
        if sort_by == "Title":
            entries.sort(key=lambda x: get_entry_field(x, 'title') or '')
        elif sort_by == "Size":
            entries.sort(key=lambda x: get_entry_field(x, 'file_size') or 0, reverse=True)
        
        # Pagination
        total_entries = len(entries)
        if total_entries > 0:
            pages = (total_entries - 1) // entries_per_page + 1
            page_num = st.selectbox("📄 Page", range(1, pages + 1)) if pages > 1 else 1
            
            start_idx = (page_num - 1) * entries_per_page
            end_idx = start_idx + entries_per_page
            page_entries = entries[start_idx:end_idx]
            
            st.write(f"Showing {start_idx + 1}-{min(end_idx, total_entries)} of {total_entries} entries")
            
            # Display entries in a grid
            cols_per_row = 3
            for i in range(0, len(page_entries), cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    if i + j < len(page_entries):
                        with cols[j]:
                            display_image_card(page_entries[i + j])
        else:
            st.info("No entries found matching your criteria.")

    elif page == "⭐ Favorites":
        st.title("⭐ My Favorites")
        
        favorites = [e for e in get_entries(username=username) if get_entry_field(e, 'is_favorite')]
        
        if favorites:
            st.write(f"You have {len(favorites)} favorite entries")
            
            # Display favorites
            for entry in favorites:
                display_image_card(entry, show_edit_controls=True)
        else:
            st.info("No favorite entries yet. Mark entries as favorites to see them here!")

    elif page == "✏️ Manage Entries":
        st.title("✏️ Manage Entries")
        
        # Bulk operations
        with st.expander("🔧 Bulk Operations"):
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📦 Archive All Selected"):
                    st.info("Bulk archive functionality would go here")
            with col2:
                if st.button("⭐ Favorite All Selected"):
                    st.info("Bulk favorite functionality would go here")
            with col3:
                if st.button("🗑️ Delete All Selected"):
                    st.info("Bulk delete functionality would go here")
        
        # Show all entries with edit controls
        all_entries = get_entries(username=username)
        
        if all_entries:
            st.write(f"Managing {len(all_entries)} entries")
            
            for entry in all_entries:
                entry_id = get_entry_field(entry, 'id')
                
                # Check if we're editing this entry
                if st.session_state.get(f'edit_entry_{entry_id}'):
                    st.subheader(f"✏️ Editing Entry #{entry_id}")
                    
                    with st.form(f"edit_form_{entry_id}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            new_title = st.text_input("Title", value=get_entry_field(entry, 'title') or '')
                            new_description = st.text_area("Description", 
                                                         value=get_entry_field(entry, 'description') or '')
                            new_categories = st.text_input("Categories", 
                                                         value=get_entry_field(entry, 'categories') or '')
                        
                        with col2:
                            new_tags = st.text_input("Tags", value=get_entry_field(entry, 'tags') or '')
                            new_notes = st.text_area("Notes", value=get_entry_field(entry, 'notes') or '')
                            new_is_favorite = st.checkbox("Favorite", 
                                                        value=bool(get_entry_field(entry, 'is_favorite')))
                            new_is_archived = st.checkbox("Archived", 
                                                        value=bool(get_entry_field(entry, 'is_archived')))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("💾 Save Changes"):
                                update_data = {
                                    'title': new_title,
                                    'description': new_description,
                                    'categories': new_categories,
                                    'tags': new_tags,
                                    'notes': new_notes,
                                    'is_favorite': new_is_favorite,
                                    'is_archived': new_is_archived
                                }
                                
                                if update_entry(entry_id, update_data):
                                    st.success("Entry updated!")
                                    del st.session_state[f'edit_entry_{entry_id}']
                                    st.rerun()
                                else:
                                    st.error("Failed to update entry")
                        
                        with col2:
                            if st.form_submit_button("❌ Cancel"):
                                del st.session_state[f'edit_entry_{entry_id}']
                                st.rerun()
                else:
                    display_image_card(entry, show_edit_controls=True)
        else:
            st.info("No entries to manage yet.")

    elif page == "📊 Categories & Tags":
        st.title("📊 Categories & Tags")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📁 Categories")
            categories = get_all_categories(username)
            if categories:
                cat_df = pd.DataFrame(categories, columns=['Category', 'Count'])
                st.dataframe(cat_df, use_container_width=True)
                
                # Category management
                st.subheader("Manage Categories")
                selected_cat = st.selectbox("Select category to rename/delete", 
                                          [cat[0] for cat in categories])
                
                col1a, col1b = st.columns(2)
                with col1a:
                    if st.button("🏷️ Rename Category"):
                        st.info("Category rename functionality would go here")
                with col1b:
                    if st.button("🗑️ Delete Category"):
                        st.info("Category delete functionality would go here")
            else:
                st.info("No categories found")
        
        with col2:
            st.subheader("🏷️ Tags")
            tags = get_all_tags(username)
            if tags:
                tags_df = pd.DataFrame(tags, columns=['Tag', 'Count'])
                st.dataframe(tags_df, use_container_width=True)
                
                # Tag management
                st.subheader("Manage Tags")
                selected_tag = st.selectbox("Select tag to rename/delete", 
                                          [tag[0] for tag in tags])
                
                col2a, col2b = st.columns(2)
                with col2a:
                    if st.button("🏷️ Rename Tag"):
                        st.info("Tag rename functionality would go here")
                with col2b:
                    if st.button("🗑️ Delete Tag"):
                        st.info("Tag delete functionality would go here")
            else:
                st.info("No tags found")

    # Footer
    st.markdown("---")
    st.markdown("*Image Knowledge Base - Powered by AI* 🤖")
