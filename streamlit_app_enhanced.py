# streamlit_app_enhanced.py - Enhanced Knowledge Base Version
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

# Helper functions for entry field access (updated for new schema)
def get_entry_field(entry, field_name):
    """Safely get a field from an entry tuple"""
    field_mapping = {
        'id': 0, 'username': 1, 'title': 2, 'filename': 3, 'description': 4, 
        'image_caption': 5, 'link': 6, 'link_summary': 7, 'categories': 8, 'tags': 9,
        'file_path': 10, 'file_size': 11, 'image_width': 12, 'image_height': 13,
        'notes': 14, 'is_favorite': 15, 'is_archived': 16, 'created_at': 17,
        'updated_at': 18, 'uploaded_at': 19
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

def display_image_from_path(file_path, caption="", use_column_width=True, width=None):
    """Display image from file path"""
    if file_path and os.path.exists(file_path):
        try:
            image = Image.open(file_path)
            if width:
                st.image(image, caption=caption, width=width)
            else:
                st.image(image, caption=caption, use_column_width=use_column_width)
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
    page_title="Knowledge Base",
    page_icon="📚",
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
    user_id = current_user['user_id']
    
    # Sidebar with user info and navigation
    with st.sidebar:
        st.success(f"Welcome, {name}! 👋")
        
        # User stats
        stats = get_user_stats(username)
        st.metric("Total Entries", stats['total_entries'])
        st.metric("Storage Used (MB)", stats['total_size_mb'])
        
        st.markdown("---")
        
        # Navigation
        page = st.selectbox("Navigate", [
            "🖼️ Add Entry", 
            "📊 Dashboard", 
            "🔍 Search & Browse",
            "⭐ Favorites", 
            "📝 Manage Entries",
            "🗂️ Categories & Tags"
        ])
        
        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            logout()

    # PAGE: Add Entry
    if page == "🖼️ Add Entry":
        st.title("🖼️ Add New Knowledge Entry")
        
        # Get existing categories and tags for suggestions
        existing_categories = get_all_categories(user_id)
        existing_tags = get_all_tags(user_id)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Basic Information
            st.subheader("📝 Basic Information")
            title = st.text_input("Title*", placeholder="Give your entry a descriptive title")
            description = st.text_area("Description", placeholder="Detailed description of the content")
            notes = st.text_area("Notes", placeholder="Additional notes or observations")
            
            # Categories and Tags
            st.subheader("🏷️ Organization")
            
            # Categories with suggestions
            if existing_categories:
                selected_categories = st.multiselect("Categories", 
                                                   options=existing_categories,
                                                   help="Select existing categories")
                new_categories = st.text_input("New Categories", 
                                             placeholder="Enter new categories separated by commas")
                
                all_categories = selected_categories.copy()
                if new_categories:
                    all_categories.extend([cat.strip() for cat in new_categories.split(',')])
            else:
                categories_input = st.text_input("Categories", 
                                               placeholder="Enter categories separated by commas")
                all_categories = [cat.strip() for cat in categories_input.split(',')] if categories_input else []
            
            # Tags with suggestions
            if existing_tags:
                selected_tags = st.multiselect("Tags", 
                                             options=existing_tags,
                                             help="Select existing tags")
                new_tags = st.text_input("New Tags", 
                                        placeholder="Enter new tags separated by commas")
                
                all_tags = selected_tags.copy()
                if new_tags:
                    all_tags.extend([tag.strip() for tag in new_tags.split(',')])
                tags_str = ", ".join(all_tags)
            else:
                tags_str = st.text_input("Tags", 
                                       placeholder="Enter tags separated by commas")
            
            # Link
            link = st.text_input("Related Link", placeholder="https://example.com")
        
        with col2:
            # Image Upload
            st.subheader("🖼️ Image Upload")
            uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "gif", "bmp"])
            
            if uploaded_file:
                st.image(uploaded_file, caption="Preview", use_column_width=True)
                
                # Auto-analyze button
                if st.button("🤖 Auto-Analyze Image", use_container_width=True):
                    with st.spinner("Analyzing image..."):
                        try:
                            result = analyze_image(uploaded_file, description, link)
                            
                            st.success("✅ Analysis complete!")
                            
                            with st.expander("🔍 AI Analysis Results"):
                                st.write("**Caption:**", result.get('caption', 'N/A'))
                                st.write("**Summary:**", result.get('summary', 'N/A'))
                                st.write("**Suggested Categories:**", ', '.join(result.get('categories', [])))
                                st.write("**Full Analysis:**", result.get('full_analysis', 'N/A'))
                                
                                # Buttons to use AI suggestions
                                col1, col2 = st.columns(2)
                                with col1:
                                    if st.button("Use AI Title"):
                                        st.session_state['use_ai_title'] = result.get('caption', '')
                                        st.rerun()
                                with col2:
                                    if st.button("Use AI Description"):
                                        st.session_state['use_ai_desc'] = result.get('summary', '')
                                        st.rerun()
                        
                        except Exception as e:
                            st.error(f"Analysis error: {str(e)}")
        
        # Apply AI suggestions if chosen
        if 'use_ai_title' in st.session_state:
            title = st.session_state['use_ai_title']
            del st.session_state['use_ai_title']
        
        if 'use_ai_desc' in st.session_state:
            description = st.session_state['use_ai_desc']
            del st.session_state['use_ai_desc']
        
        st.markdown("---")
        
        # Save Entry
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("💾 Save Entry", use_container_width=True, type="primary"):
                if not title:
                    st.error("Title is required!")
                else:
                    with st.spinner("Saving entry..."):
                        try:
                            # If there's an image, analyze it for summary
                            summary = description
                            if uploaded_file:
                                try:
                                    result = analyze_image(uploaded_file, description, link)
                                    summary = result.get('summary', description)
                                except:
                                    summary = description
                            
                            success, message = insert_data(
                                username=username,
                                image_file=uploaded_file,
                                description=description,
                                link=link,
                                summary=summary,
                                categories=all_categories,
                                title=title,
                                tags=tags_str,
                                notes=notes
                            )
                            
                            if success:
                                st.success("✅ Entry saved successfully!")
                                st.balloons()
                                
                                # Clear form
                                if st.button("➕ Add Another Entry"):
                                    st.rerun()
                            else:
                                st.error(f"❌ Error saving: {message}")
                                
                        except Exception as e:
                            st.error(f"Error: {str(e)}")

    # PAGE: Dashboard
    elif page == "📊 Dashboard":
        st.title("📊 Knowledge Base Dashboard")
        
        # User statistics
        stats = get_user_stats(username)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Entries", stats['total_entries'])
        with col2:
            st.metric("Storage Used", f"{stats['total_size_mb']} MB")
        with col3:
            categories = get_all_categories(user_id)
            st.metric("Categories", len(categories))
        with col4:
            tags = get_all_tags(user_id)
            st.metric("Tags", len(tags))
        
        st.markdown("---")
        
        # Recent entries
        st.subheader("📝 Recent Entries")
        recent_entries = search_entries(user_id, limit=6)
        
        if recent_entries:
            # Display in cards format
            for i in range(0, len(recent_entries), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    if i + j < len(recent_entries):
                        entry = recent_entries[i + j]
                        with col:
                            with st.container():
                                # Display image if available
                                file_path = get_entry_field(entry, 'file_path')
                                if file_path:
                                    display_image_from_path(file_path, width=200)
                                
                                title = get_entry_field(entry, 'title') or 'Untitled'
                                st.write(f"**{title}**")
                                
                                description = get_entry_field(entry, 'description')
                                if description:
                                    st.write(description[:100] + "..." if len(description) > 100 else description)
                                
                                uploaded_at = get_entry_field(entry, 'uploaded_at')
                                if uploaded_at:
                                    st.caption(f"📅 {uploaded_at[:10]}")
                                
                                # Quick actions
                                entry_id = get_entry_field(entry, 'id')
                                if st.button(f"👁️ View", key=f"view_{entry_id}"):
                                    st.session_state['view_entry_id'] = entry_id
                                    st.session_state['page'] = "📝 Manage Entries"
                                    st.rerun()
        else:
            st.info("No entries yet. Start by adding your first entry!")

    # PAGE: Search & Browse
    elif page == "🔍 Search & Browse":
        st.title("🔍 Search & Browse Knowledge Base")
        
        # Search filters
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search_term = st.text_input("🔍 Search", placeholder="Search in titles, descriptions, notes...")
        with col2:
            categories = get_all_categories(user_id)
            category_filter = st.selectbox("Category", ["All"] + categories)
            category_filter = None if category_filter == "All" else category_filter
        with col3:
            tags = get_all_tags(user_id)
            tag_filter = st.selectbox("Tag", ["All"] + tags)
            tag_filter = None if tag_filter == "All" else tag_filter
        
        # Additional filters
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            sort_by = st.selectbox("Sort by", ["uploaded_at", "updated_at", "title", "created_at"])
        with col2:
            sort_order = st.selectbox("Order", ["DESC", "ASC"])
        with col3:
            show_favorites = st.checkbox("⭐ Favorites only")
        with col4:
            show_archived = st.checkbox("📦 Include archived")
        
        # Search
        entries = search_entries(
            user_id=user_id,
            search_term=search_term,
            category_filter=category_filter,
            tag_filter=tag_filter,
            is_favorite=True if show_favorites else None,
            is_archived=True if show_archived else False,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        st.write(f"Found {len(entries)} entries")
        
        # Display results
        if entries:
            for entry in entries:
                with st.expander(f"📄 {get_entry_field(entry, 'title') or 'Untitled'}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        # Entry details
                        description = get_entry_field(entry, 'description')
                        if description:
                            st.write("**Description:**", description)
                        
                        notes = get_entry_field(entry, 'notes')
                        if notes:
                            st.write("**Notes:**", notes)
                        
                        categories = get_entry_field(entry, 'categories')
                        if categories:
                            st.write("**Categories:**", categories)
                        
                        tags = get_entry_field(entry, 'tags')
                        if tags:
                            st.write("**Tags:**", tags)
                        
                        link = get_entry_field(entry, 'link')
                        if link:
                            st.write("**Link:**", link)
                    
                    with col2:
                        # Image and metadata
                        file_path = get_entry_field(entry, 'file_path')
                        if file_path:
                            display_image_from_path(file_path, width=200)
                        
                        uploaded_at = get_entry_field(entry, 'uploaded_at')
                        if uploaded_at:
                            st.write("📅", uploaded_at[:16])
                        
                        file_size = get_entry_field(entry, 'file_size')
                        if file_size:
                            st.write("📊", format_file_size(file_size))
                        
                        # Actions
                        entry_id = get_entry_field(entry, 'id')
                        is_favorite = get_entry_field(entry, 'is_favorite')
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            fav_text = "💔 Unfavorite" if is_favorite else "⭐ Favorite"
                            if st.button(fav_text, key=f"fav_{entry_id}"):
                                update_entry(entry_id, user_id, is_favorite=not is_favorite)
                                st.rerun()
                        with col2:
                            if st.button("✏️ Edit", key=f"edit_{entry_id}"):
                                st.session_state['edit_entry_id'] = entry_id
                                st.session_state['page'] = "📝 Manage Entries"
                                st.rerun()
        else:
            st.info("No entries found matching your criteria.")

    # PAGE: Favorites
    elif page == "⭐ Favorites":
        st.title("⭐ Your Favorite Entries")
        
        favorites = search_entries(user_id=user_id, is_favorite=True)
        
        if favorites:
            st.write(f"You have {len(favorites)} favorite entries")
            
            for entry in favorites:
                with st.container():
                    col1, col2, col3 = st.columns([1, 2, 1])
                    
                    with col1:
                        file_path = get_entry_field(entry, 'file_path')
                        if file_path:
                            display_image_from_path(file_path, width=150)
                    
                    with col2:
                        title = get_entry_field(entry, 'title') or 'Untitled'
                        st.write(f"**{title}**")
                        
                        description = get_entry_field(entry, 'description')
                        if description:
                            st.write(description[:200] + "..." if len(description) > 200 else description)
                        
                        categories = get_entry_field(entry, 'categories')
                        if categories:
                            st.write(f"🏷️ {categories}")
                    
                    with col3:
                        uploaded_at = get_entry_field(entry, 'uploaded_at')
                        if uploaded_at:
                            st.write(f"📅 {uploaded_at[:10]}")
                        
                        entry_id = get_entry_field(entry, 'id')
                        if st.button("💔 Remove from Favorites", key=f"unfav_{entry_id}"):
                            update_entry(entry_id, user_id, is_favorite=False)
                            st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("No favorite entries yet. Mark entries as favorites to see them here!")

    # PAGE: Manage Entries (Edit/Delete)
    elif page == "📝 Manage Entries":
        st.title("📝 Manage Your Entries")
        
        # Check if we're editing a specific entry
        if 'edit_entry_id' in st.session_state:
            entry_id = st.session_state['edit_entry_id']
            entry = get_entry_by_id(entry_id, user_id)
            
            if entry:
                st.subheader(f"✏️ Editing: {get_entry_field(entry, 'title')}")
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    # Editable fields
                    new_title = st.text_input("Title", value=get_entry_field(entry, 'title') or "")
                    new_description = st.text_area("Description", value=get_entry_field(entry, 'description') or "")
                    new_notes = st.text_area("Notes", value=get_entry_field(entry, 'notes') or "")
                    new_categories = st.text_input("Categories", value=get_entry_field(entry, 'categories') or "")
                    new_tags = st.text_input("Tags", value=get_entry_field(entry, 'tags') or "")
                    new_link = st.text_input("Link", value=get_entry_field(entry, 'link') or "")
                
                with col2:
                    # Show current image
                    file_path = get_entry_field(entry, 'file_path')
                    if file_path:
                        st.write("**Current Image:**")
                        display_image_from_path(file_path)
                    
                    # Quick info
                    st.write("**Entry Info:**")
                    st.write(f"Created: {get_entry_field(entry, 'created_at')[:16]}")
                    st.write(f"Updated: {get_entry_field(entry, 'updated_at')[:16]}")
                    
                    file_size = get_entry_field(entry, 'file_size')
                    if file_size:
                        st.write(f"File Size: {format_file_size(file_size)}")
                
                st.markdown("---")
                
                # Action buttons
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("💾 Save Changes", type="primary"):
                        success, message = update_entry(
                            entry_id, user_id,
                            title=new_title,
                            description=new_description,
                            notes=new_notes,
                            categories=new_categories,
                            tags=new_tags,
                            link=new_link
                        )
                        
                        if success:
                            st.success("✅ Entry updated successfully!")
                            del st.session_state['edit_entry_id']
                            st.rerun()
                        else:
                            st.error(f"❌ Error: {message}")
                
                with col2:
                    is_favorite = get_entry_field(entry, 'is_favorite')
                    fav_text = "💔 Remove Favorite" if is_favorite else "⭐ Add Favorite"
                    if st.button(fav_text):
                        update_entry(entry_id, user_id, is_favorite=not is_favorite)
                        st.rerun()
                
                with col3:
                    is_archived = get_entry_field(entry, 'is_archived')
                    arch_text = "📤 Unarchive" if is_archived else "📦 Archive"
                    if st.button(arch_text):
                        update_entry(entry_id, user_id, is_archived=not is_archived)
                        st.rerun()
                
                with col4:
                    if st.button("🗑️ Delete Entry", type="secondary"):
                        st.session_state['confirm_delete'] = entry_id
                
                # Confirm delete
                if st.session_state.get('confirm_delete') == entry_id:
                    st.error("⚠️ Are you sure you want to delete this entry? This action cannot be undone.")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Yes, Delete", type="primary"):
                            success, message = delete_entry(entry_id, user_id)
                            if success:
                                st.success("Entry deleted successfully!")
                                del st.session_state['edit_entry_id']
                                del st.session_state['confirm_delete']
                                st.rerun()
                            else:
                                st.error(f"Error: {message}")
                    with col2:
                        if st.button("❌ Cancel"):
                            del st.session_state['confirm_delete']
                            st.rerun()
                
                # Back button
                if st.button("← Back to Browse"):
                    del st.session_state['edit_entry_id']
                    st.session_state['page'] = "🔍 Search & Browse"
                    st.rerun()
            else:
                st.error("Entry not found!")
                del st.session_state['edit_entry_id']
        else:
            # Show all entries for management
            st.write("Select an entry to edit from the Search & Browse page, or manage bulk operations here.")
            
            # Bulk operations
            entries = get_entries(user_id=user_id)
            if entries:
                st.write(f"You have {len(entries)} total entries")
                
                # Simple list view
                for entry in entries[:10]:  # Show first 10
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        title = get_entry_field(entry, 'title') or 'Untitled'
                        st.write(f"**{title}**")
                        uploaded_at = get_entry_field(entry, 'uploaded_at')
                        if uploaded_at:
                            st.caption(f"📅 {uploaded_at[:10]}")
                    
                    with col2:
                        entry_id = get_entry_field(entry, 'id')
                        if st.button("✏️ Edit", key=f"manage_edit_{entry_id}"):
                            st.session_state['edit_entry_id'] = entry_id
                            st.rerun()
                    
                    with col3:
                        is_favorite = get_entry_field(entry, 'is_favorite')
                        fav_icon = "⭐" if is_favorite else "☆"
                        st.write(fav_icon)

    # PAGE: Categories & Tags
    elif page == "🗂️ Categories & Tags":
        st.title("🗂️ Categories & Tags Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📁 Categories")
            categories = get_all_categories(user_id)
            
            if categories:
                for category in categories:
                    # Count entries in this category
                    entries_with_cat = search_entries(user_id, category_filter=category)
                    st.write(f"**{category}** ({len(entries_with_cat)} entries)")
            else:
                st.info("No categories yet. Add entries with categories to see them here.")
        
        with col2:
            st.subheader("🏷️ Tags")
            tags = get_all_tags(user_id)
            
            if tags:
                for tag in tags:
                    # Count entries with this tag
                    entries_with_tag = search_entries(user_id, tag_filter=tag)
                    st.write(f"**{tag}** ({len(entries_with_tag)} entries)")
            else:
                st.info("No tags yet. Add entries with tags to see them here.")
        
        st.markdown("---")
        st.info("💡 **Tip:** Use the Search & Browse page to filter entries by categories and tags.")
