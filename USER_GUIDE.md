# User Guide - Image Knowledge Base

## Getting Started

### First Time Login

1. **Open the Application**
   - Navigate to `http://localhost:8501` in your browser
   - You'll see the login page

2. **Create Your Account**
   - Click "Sign Up" or create account option
   - Enter your details:
     - Username (unique identifier)
     - Email address
     - Full name
     - Password (will be securely encrypted)
   - Click "Create Account"

3. **Login**
   - Enter your username and password
   - Click "Login"

## Main Interface Overview

### Sidebar Navigation

The sidebar contains:
- **Welcome Message** - Shows your name
- **Statistics** - Total uploads and storage used
- **Navigation Menu** - Access different sections
- **Logout Button** - Safely exit the application

### Navigation Options

- 🖼️ **Add Entry** - Upload new images
- 📊 **Dashboard** - Overview and quick access
- 🔍 **Search & Browse** - Advanced search and filtering
- ⭐ **Favorites** - Your favorite images
- 📝 **Manage Entries** - Edit and organize your collection

## 🖼️ Adding Images

### Upload Process

1. **Navigate to Add Entry**
   - Click "🖼️ Add Entry" in the sidebar

2. **Upload Your Image**
   - Click "Upload Image" button
   - Select image file (JPG, PNG, GIF, BMP)
   - Preview appears immediately

3. **Add Information**
   - **Title** (optional) - Give your image a descriptive name
   - **Description** - Detailed description of the image
   - **Categories** - Comma-separated (e.g., "nature, landscape, travel")
   - **Tags** - Comma-separated (e.g., "sunset, mountains, vacation")
   - **Link** - Related URL (optional)
   - **Notes** - Additional notes or context

4. **AI Analysis** (Recommended)
   - Keep "Use AI for automatic analysis" checked
   - AI will automatically analyze your image and suggest:
     - Detailed description
     - Relevant categories
     - Object identification

5. **Save Options**
   - Check "Mark as favorite" for important images
   - Click "🚀 Add Entry" to save

### AI Features

The AI analysis provides:
- **Object Recognition** - Identifies people, objects, scenes
- **Color Analysis** - Dominant colors and composition
- **Scene Description** - Detailed description of what's happening
- **Category Suggestions** - Automatic categorization
- **Content Analysis** - Text extraction if present in image

## 📊 Dashboard Features

### Statistics Overview
- **Total Entries** - Number of images in your collection
- **Storage Used** - Total disk space consumed
- **Favorites** - Count of favorite images
- **Last Upload** - When you last added an image

### Image Gallery
- **Thumbnail Grid** - Visual preview of recent images
- **Quick Actions** - Favorite/unfavorite directly from thumbnails
- **Star Indicators** - Shows which images are favorites

### Quick Search
- Search across titles, descriptions, tags, and categories
- Results show with image previews
- Click to view full details

### Recent Entries
- Last 5 uploaded images
- Expandable details with full information
- Quick action buttons for each entry

## 🔍 Advanced Search & Browse

### Search Options

1. **Text Search**
   - Search in titles, descriptions, notes
   - Case-insensitive matching
   - Partial word matching

2. **Category Filter**
   - Dropdown of all your categories
   - Select "All" to see everything

3. **Tag Filter**
   - Dropdown of all your tags
   - Combine with text search for precision

4. **Special Filters**
   - ⭐ **Favorites Only** - Show only starred images
   - 📦 **Show Archived** - Include archived entries
   - **Sort Options** - By date, title, or file size
   - **Per Page** - Control how many results to show

### Search Results

- **Grid Layout** - Images with details
- **Quick Actions** - Favorite and edit buttons
- **Pagination** - Navigate through large result sets
- **Metadata Display** - Creation date, file size, dimensions

## ⭐ Managing Favorites

### Adding Favorites
- **During Upload** - Check "Mark as favorite"
- **From Dashboard** - Click heart icon on thumbnails
- **From Search** - Click heart icon in results
- **From Any View** - Heart icons are everywhere

### Favorites Page
- View all your favorite images
- Quick unfavorite option
- Edit favorites directly
- Special star indicators

### Why Use Favorites?
- Quick access to important images
- Create curated collections
- Mark images for later review
- Organize by importance

## 📝 Managing Your Collection

### Editing Entries

1. **Navigate to Manage Entries**
   - Click "📝 Manage Entries" in sidebar

2. **Select Entry to Edit**
   - Click "✏️ Edit" button on any entry

3. **Edit Information**
   - Modify title, description, categories, tags
   - Add or update notes
   - Change favorite/archive status

4. **Save Changes**
   - Click "💾 Save Changes"
   - Or "❌ Cancel" to discard

### Deleting Entries

1. **Find the Entry**
   - Use Manage Entries or Search

2. **Delete Process**
   - Click "🗑️ Delete" button
   - Click again to confirm deletion
   - Both database entry and image file are removed

### Archiving

- Mark entries as archived instead of deleting
- Archived entries don't appear in normal searches
- Use "Show archived" filter to view them
- Good for old or less relevant images

## 🏷️ Organization Tips

### Effective Tagging

1. **Be Consistent**
   - Use the same terms (e.g., "landscape" not "landscapes")
   - Create a personal tagging system

2. **Use Hierarchies**
   - Broad to specific: "travel, europe, france, paris"
   - Objects to details: "food, dinner, pasta, italian"

3. **Include Context**
   - When: "2023, summer, vacation"
   - Where: "home, office, outdoors"
   - Who: "family, friends, work"

### Categories vs Tags

- **Categories** - Broad classifications (nature, work, family)
- **Tags** - Specific descriptors (sunset, meeting, birthday)
- Use both for maximum organization

### Search Strategies

1. **Start Broad** - Use categories first
2. **Add Filters** - Narrow with tags or text
3. **Use Favorites** - For frequently accessed images
4. **Sort Results** - By date for chronological view

## 🔧 Settings & Preferences

### Account Management
- View your profile in the sidebar
- Monitor storage usage
- Track upload statistics

### Data Management
- Regular backup recommended
- Archive old entries to save space
- Delete duplicates or unwanted images

## 🚨 Troubleshooting

### Common Issues

**Images Not Uploading**
- Check file format (JPG, PNG, GIF, BMP supported)
- Verify file size (default limit is ~200MB)
- Ensure stable internet connection

**AI Analysis Not Working**
- Check internet connection
- Verify API key is configured
- Try uploading without AI analysis

**Search Not Finding Images**
- Check spelling in search terms
- Try broader search terms
- Use category/tag filters instead

**Slow Performance**
- Close other browser tabs
- Restart the application
- Check available disk space

### Best Practices

1. **Regular Organization**
   - Review and tag new uploads weekly
   - Clean up old or duplicate entries
   - Update categories as your collection grows

2. **Backup Strategy**
   - Export important images regularly
   - Note down your tagging system
   - Keep API keys secure

3. **Efficient Workflow**
   - Use batch uploads for similar images
   - Develop consistent naming conventions
   - Leverage AI analysis for initial categorization

## 📱 Mobile Usage

The application is responsive and works on mobile devices:
- Touch-friendly interface
- Optimized image viewing
- Mobile camera uploads supported
- Swipe gestures for navigation

## 🔒 Privacy & Security

- All data stored locally on your machine
- Passwords encrypted with bcrypt
- Images processed securely
- No data sent to third parties (except AI analysis)

---

**Happy organizing! Your images are now searchable and beautifully managed! 🖼️✨**
