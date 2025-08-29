import streamlit as st
import os
from PIL import Image
from components.image_processor import analyze_image
from components.db import (insert_data, init_db, get_user_stats, get_entries, 
                          update_entry, delete_entry, get_entry_by_id, search_entries,
                          get_all_categories, get_all_tags)
from components.auth import login_form, logout, check_authentication, get_current_user

# --- Load environment variables ---
from dotenv import load_dotenv
load_dotenv()

# Helper functions for entry field access (updated for current schema)
def get_entry_field(entry, field_name):
    """Safely get a field from an entry tuple"""
    field_mapping = {
        'id': 0, 'username': 1, 'filename': 2, 'description': 3, 
        'image_caption': 4, 'link': 5, 'link_summary': 6, 'categories': 7,
        'uploaded_at': 8, 'user_id': 9, 'file_path': 10, 'file_size': 11,
        'title': 12, 'tags': 13, 'image_width': 14, 'image_height': 15,
        'notes': 16, 'is_favorite': 17, 'is_archived': 18
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

def display_image_from_path(file_path, caption="", use_container_width=True):
    """Display image from file path"""
    if file_path and os.path.exists(file_path):
        try:
            image = Image.open(file_path)
            st.image(image, caption=caption, use_container_width=use_container_width)
            return True
        except Exception as e:
            st.error(f"Error loading image: {e}")
    else:
        st.warning("Image file not found")
    return False

# Initialize database
init_db()

# Configure page
st.set_page_config(
    page_title="Image Analyzer",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = False

# Authentication check
if not check_authentication():
    # Show login form if not authenticated
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
        st.metric("Total Uploads", stats['total_entries'])
        st.metric("Storage Used (MB)", stats['total_size_mb'])
        
        st.markdown("---")
        
        # Navigation
        page = st.selectbox("Navigate", [
            "🖼️ Add Entry", 
            "📊 Dashboard", 
            "� Search & Browse",
            "⭐ Favorites", 
            "📝 Manage Entries"
        ])
        
        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            logout()

    if page == "🖼️ Add Entry":
        st.title("🖼️ Add New Entry")
        
        with st.form("add_entry_form"):
            col1, col2 = st.columns([1, 1])
            
            with col1:
                # Image upload
                uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png", "gif", "bmp"])
                
                if uploaded_file:
                    st.image(uploaded_file, caption="Preview", use_container_width=True)
                
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

    elif page == "📊 Dashboard":
        st.title("📊 Dashboard")
        
        # User statistics
        stats = get_user_stats(username)
        user_entries = get_entries(username=username)
        favorites_count = sum(1 for entry in user_entries if get_entry_field(entry, 'is_favorite'))
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Entries", stats['total_entries'])
        with col2:
            st.metric("Storage Used", f"{stats['total_size_mb']} MB")
        with col3:
            st.metric("Favorites", favorites_count)
        with col4:
            if stats['last_upload']:
                st.metric("Last Upload", stats['last_upload'][:10])
            else:
                st.metric("Last Upload", "Never")
        
        st.markdown("---")
        
        # Image Gallery Preview
        st.subheader("🖼️ Recent Images Gallery")
        gallery_entries = get_entries(username=username, limit=12)
        
        if gallery_entries:
            # Create a grid layout for thumbnails
            cols_per_row = 4
            for i in range(0, len(gallery_entries), cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    if i + j < len(gallery_entries):
                        entry = gallery_entries[i + j]
                        with cols[j]:
                            file_path = get_entry_field(entry, 'file_path')
                            title = get_entry_field(entry, 'title') or get_entry_field(entry, 'filename') or 'Unknown'
                            entry_id = get_entry_field(entry, 'id')
                            is_favorite = get_entry_field(entry, 'is_favorite')
                            
                            if file_path and os.path.exists(file_path):
                                # Display image with title
                                st.image(file_path, caption=f"{'⭐' if is_favorite else ''}{title[:20]}..." if len(title) > 20 else f"{'⭐' if is_favorite else ''}{title}", use_container_width=True)
                                
                                # Quick favorite toggle
                                if st.button(f"{'💔' if is_favorite else '❤️'}", key=f"gallery_fav_{entry_id}", help="Toggle favorite", use_container_width=True):
                                    update_entry(entry_id, {'is_favorite': not is_favorite})
                                    st.rerun()
                            else:
                                st.info("🖼️ No image")
                                st.caption(title)
        else:
            st.info("No images yet. Upload some images to see them here!")
        
        st.markdown("---")
        
        # Search box on dashboard
        st.subheader("🔍 Quick Search")
        search_query = st.text_input("Search your entries...", placeholder="Search titles, descriptions, tags...")
        
        if search_query:
            # Perform search
            search_results = []
            for entry in user_entries:
                title = get_entry_field(entry, 'title') or ''
                description = get_entry_field(entry, 'description') or ''
                tags = get_entry_field(entry, 'tags') or ''
                categories = get_entry_field(entry, 'categories') or ''
                
                if (search_query.lower() in title.lower() or 
                    search_query.lower() in description.lower() or
                    search_query.lower() in tags.lower() or
                    search_query.lower() in categories.lower()):
                    search_results.append(entry)
            
            st.write(f"Found {len(search_results)} results for '{search_query}'")
            
            for entry in search_results[:5]:  # Show top 5 results
                with st.expander(f"📄 {get_entry_field(entry, 'title') or get_entry_field(entry, 'filename')}", expanded=False):
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        file_path = get_entry_field(entry, 'file_path')
                        if file_path and os.path.exists(file_path):
                            st.image(file_path, width=200)
                        else:
                            st.info("🖼️ Image not available")
                    with col2:
                        description = get_entry_field(entry, 'description')
                        if description:
                            st.write(f"**Description:** {description[:200]}...")
                        
                        tags = get_entry_field(entry, 'tags')
                        if tags:
                            st.write(f"**Tags:** {tags}")
                        
                        categories = get_entry_field(entry, 'categories')
                        if categories:
                            st.write(f"**Categories:** {categories}")
                        
                        # Quick action to view full entry
                        entry_id = get_entry_field(entry, 'id')
                        if st.button(f"View Full Entry", key=f"search_view_{entry_id}"):
                            st.session_state['page'] = "🔍 Search & Browse"
                            st.rerun()
        
        # Recent entries
        st.subheader("📈 Recent Entries")
        recent_entries = get_entries(username=username, limit=5)
        
        if recent_entries:
            for entry in recent_entries:
                filename = get_entry_field(entry, 'filename') or 'Unknown'
                title = get_entry_field(entry, 'title') or filename
                uploaded_at = get_entry_field(entry, 'uploaded_at') or ''
                
                with st.expander(f"📄 {title} - {uploaded_at[:10]}", expanded=False):
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        file_path = get_entry_field(entry, 'file_path')
                        if file_path and os.path.exists(file_path):
                            st.image(file_path, width=200, caption=filename)
                        else:
                            st.info("🖼️ Image not available")
                    
                    with col2:
                        description = get_entry_field(entry, 'description')
                        if description:
                            st.write(f"**Description:** {description}")
                        
                        categories = get_entry_field(entry, 'categories')
                        if categories:
                            st.write(f"**Categories:** {categories}")
                        
                        tags = get_entry_field(entry, 'tags')
                        if tags:
                            st.write(f"**Tags:** {tags}")
                        
                        file_size = get_entry_field(entry, 'file_size')
                        if file_size:
                            st.write(f"**Size:** {format_file_size(file_size)}")
                        
                        # Quick actions in dashboard
                        col2a, col2b, col2c = st.columns(3)
                        with col2a:
                            is_favorite = get_entry_field(entry, 'is_favorite')
                            entry_id = get_entry_field(entry, 'id')
                            if st.button(f"{'💔' if is_favorite else '❤️'}", key=f"dash_fav_{entry_id}", help="Toggle favorite"):
                                update_entry(entry_id, {'is_favorite': not is_favorite})
                                st.rerun()
                        with col2b:
                            if st.button(f"✏️", key=f"dash_edit_{entry_id}", help="Edit entry"):
                                st.session_state[f'edit_entry_{entry_id}'] = True
                                st.rerun()
                        with col2c:
                            if st.button(f"🔍", key=f"dash_view_{entry_id}", help="View in Search"):
                                st.session_state['page'] = "🔍 Search & Browse"
                                st.rerun()
        else:
            st.info("No entries yet. Start by adding your first image!")

    elif page == "🔍 Search & Browse":
        st.title("🔍 Search & Browse")
        
        # Search and filter controls
        with st.expander("🔧 Search & Filter Options", expanded=True):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                search_query = st.text_input("🔍 Search in titles, descriptions, notes...", 
                                           placeholder="Enter search terms")
            
            with col2:
                all_categories = get_all_categories(username)
                category_filter = st.selectbox("📁 Category", ["All"] + all_categories)
            
            with col3:
                all_tags = get_all_tags(username)
                tag_filter = st.selectbox("🏷️ Tag", ["All"] + all_tags)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                show_favorites = st.checkbox("⭐ Favorites only")
            with col2:
                show_archived = st.checkbox("📦 Show archived")
            with col3:
                sort_by = st.selectbox("Sort by", ["Recent", "Title", "Size"])
            with col4:
                entries_per_page = st.selectbox("Per page", [12, 24, 48])
        
        # Get entries
        all_entries = get_entries(username=username)
        
        # Apply filters
        filtered_entries = []
        for entry in all_entries:
            # Search filter
            if search_query:
                title = get_entry_field(entry, 'title') or ''
                description = get_entry_field(entry, 'description') or ''
                notes = get_entry_field(entry, 'notes') or ''
                tags = get_entry_field(entry, 'tags') or ''
                
                if not (search_query.lower() in title.lower() or 
                       search_query.lower() in description.lower() or
                       search_query.lower() in notes.lower() or
                       search_query.lower() in tags.lower()):
                    continue
            
            # Category filter
            if category_filter != "All":
                categories = get_entry_field(entry, 'categories') or ''
                if category_filter not in categories:
                    continue
            
            # Tag filter
            if tag_filter != "All":
                tags = get_entry_field(entry, 'tags') or ''
                if tag_filter not in tags:
                    continue
            
            # Favorites filter
            if show_favorites and not get_entry_field(entry, 'is_favorite'):
                continue
            
            # Archived filter
            if not show_archived and get_entry_field(entry, 'is_archived'):
                continue
            
            filtered_entries.append(entry)
        
        # Sort entries
        if sort_by == "Title":
            filtered_entries.sort(key=lambda x: get_entry_field(x, 'title') or '')
        elif sort_by == "Size":
            filtered_entries.sort(key=lambda x: get_entry_field(x, 'file_size') or 0, reverse=True)
        
        # Pagination
        total_entries = len(filtered_entries)
        if total_entries > 0:
            pages = (total_entries - 1) // entries_per_page + 1
            page_num = st.selectbox("📄 Page", range(1, pages + 1)) if pages > 1 else 1
            
            start_idx = (page_num - 1) * entries_per_page
            end_idx = start_idx + entries_per_page
            page_entries = filtered_entries[start_idx:end_idx]
            
            st.write(f"Showing {start_idx + 1}-{min(end_idx, total_entries)} of {total_entries} entries")
            
            # Display entries
            for entry in page_entries:
                with st.container():
                    col1, col2, col3 = st.columns([1, 2, 1])
                    
                    with col1:
                        file_path = get_entry_field(entry, 'file_path')
                        filename = get_entry_field(entry, 'filename') or 'Unknown'
                        display_image_from_path(file_path, filename, use_container_width=False)
                    
                    with col2:
                        title = get_entry_field(entry, 'title') or filename
                        is_favorite = get_entry_field(entry, 'is_favorite')
                        is_archived = get_entry_field(entry, 'is_archived')
                        
                        title_text = f"{'⭐' if is_favorite else ''}{'📦' if is_archived else ''} {title}"
                        st.write(f"**{title_text}**")
                        
                        description = get_entry_field(entry, 'description')
                        if description:
                            display_desc = description[:200] + "..." if len(description) > 200 else description
                            st.write(display_desc)
                        
                        tags = get_entry_field(entry, 'tags')
                        if tags:
                            st.write(f"🏷️ **Tags:** {tags}")
                        
                        categories = get_entry_field(entry, 'categories')
                        if categories:
                            st.write(f"📁 **Categories:** {categories}")
                    
                    with col3:
                        entry_id = get_entry_field(entry, 'id')
                        created_at = get_entry_field(entry, 'created_at')
                        file_size = get_entry_field(entry, 'file_size')
                        
                        if created_at:
                            st.caption(f"📅 {created_at[:16]}")
                        if file_size:
                            st.caption(f"💾 {format_file_size(file_size)}")
                        
                        # Quick actions
                        col3a, col3b = st.columns(2)
                        with col3a:
                            if st.button(f"❤️", key=f"fav_{entry_id}", help="Toggle favorite"):
                                update_entry(entry_id, {'is_favorite': not is_favorite})
                                st.rerun()
                        with col3b:
                            if st.button(f"✏️", key=f"edit_{entry_id}", help="Edit entry"):
                                st.session_state[f'edit_entry_{entry_id}'] = True
                                st.rerun()
                
                st.divider()
        else:
            st.info("No entries found matching your criteria.")

    elif page == "⭐ Favorites":
        st.title("⭐ My Favorites")
        
        favorites = [e for e in get_entries(username=username) if get_entry_field(e, 'is_favorite')]
        
        if favorites:
            st.write(f"You have {len(favorites)} favorite entries")
            
            for entry in favorites:
                with st.container():
                    col1, col2, col3 = st.columns([1, 2, 1])
                    
                    with col1:
                        file_path = get_entry_field(entry, 'file_path')
                        filename = get_entry_field(entry, 'filename') or 'Unknown'
                        display_image_from_path(file_path, filename, use_container_width=False)
                    
                    with col2:
                        title = get_entry_field(entry, 'title') or filename
                        st.write(f"**⭐ {title}**")
                        
                        description = get_entry_field(entry, 'description')
                        if description:
                            st.write(description[:200] + "..." if len(description) > 200 else description)
                        
                        tags = get_entry_field(entry, 'tags')
                        if tags:
                            st.write(f"🏷️ **Tags:** {tags}")
                    
                    with col3:
                        entry_id = get_entry_field(entry, 'id')
                        
                        if st.button(f"💔 Unfavorite", key=f"unfav_{entry_id}"):
                            update_entry(entry_id, {'is_favorite': False})
                            st.rerun()
                        
                        if st.button(f"✏️ Edit", key=f"edit_fav_{entry_id}"):
                            st.session_state[f'edit_entry_{entry_id}'] = True
                            st.rerun()
                
                st.divider()
        else:
            st.info("No favorite entries yet. Mark entries as favorites to see them here!")

    elif page == "📝 Manage Entries":
        st.title("📝 Manage Entries")
        
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
                    # Display entry with edit controls
                    with st.container():
                        col1, col2, col3 = st.columns([1, 2, 1])
                        
                        with col1:
                            file_path = get_entry_field(entry, 'file_path')
                            filename = get_entry_field(entry, 'filename') or 'Unknown'
                            display_image_from_path(file_path, filename, use_container_width=False)
                        
                        with col2:
                            title = get_entry_field(entry, 'title') or filename
                            is_favorite = get_entry_field(entry, 'is_favorite')
                            is_archived = get_entry_field(entry, 'is_archived')
                            
                            title_text = f"{'⭐' if is_favorite else ''}{'📦' if is_archived else ''} {title}"
                            st.write(f"**{title_text}**")
                            
                            description = get_entry_field(entry, 'description')
                            if description:
                                st.write(description[:150] + "..." if len(description) > 150 else description)
                        
                        with col3:
                            if st.button(f"✏️ Edit", key=f"edit_mgmt_{entry_id}"):
                                st.session_state[f'edit_entry_{entry_id}'] = True
                                st.rerun()
                            
                            if st.button(f"🗑️ Delete", key=f"del_{entry_id}"):
                                if st.session_state.get(f'confirm_delete_{entry_id}'):
                                    if delete_entry(entry_id):
                                        st.success("Entry deleted!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to delete entry")
                                else:
                                    st.session_state[f'confirm_delete_{entry_id}'] = True
                                    st.warning("Click again to confirm deletion")
                    
                    st.divider()
        else:
            st.info("No entries to manage yet.")

    # Test API functionality
    if st.sidebar.button("🔧 Test API Connection"):
        with st.spinner("Testing API..."):
            from components.gemini_client import test_api_connection
            success, message = test_api_connection()
            if success:
                st.sidebar.success(f"✅ API Working: {message}")
            else:
                st.sidebar.error(f"❌ API Error: {message}")
