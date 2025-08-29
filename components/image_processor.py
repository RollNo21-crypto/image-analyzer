from components.gemini_client import analyze_image_with_gemini, summarize_with_gemini
from PIL import Image
import io
import re

def analyze_image(uploaded_image, description="", link=""):
    """Analyze an image and return structured data"""
    try:
        # Create a comprehensive prompt for image analysis
        base_prompt = """
        Analyze this image in detail and provide:
        1. A comprehensive description of what you see
        2. Identify key objects, people, activities, or scenes
        3. Note colors, composition, and visual elements
        4. Suggest 3-5 relevant categories/tags
        """
        
        if description:
            base_prompt += f"\n\nAdditional context provided by user: {description}"
        
        if link:
            base_prompt += f"\n\nRelated link context: {link}"
        
        # Use Gemini Vision to analyze the image
        analysis_result = analyze_image_with_gemini(uploaded_image, base_prompt)
        
        # Extract categories from the analysis (simple approach)
        categories = extract_categories_from_text(analysis_result)
        
        # Generate a summary if the analysis is very long
        if len(analysis_result) > 500:
            summary_prompt = f"Provide a concise summary of this image analysis: {analysis_result}"
            summary = summarize_with_gemini(summary_prompt)
        else:
            summary = analysis_result
        
        return {
            "summary": summary,
            "categories": categories,
            "caption": extract_caption_from_text(analysis_result),
            "full_analysis": analysis_result
        }
        
    except Exception as e:
        # Fallback to basic text analysis
        error_msg = str(e)
        return {
            "summary": f"Image analysis encountered an error: {error_msg}",
            "categories": ["error", "fallback"],
            "caption": "Analysis failed",
            "full_analysis": f"Error details: {error_msg}"
        }

def extract_categories_from_text(text):
    """Extract relevant categories from analysis text"""
    # Common category keywords to look for
    category_keywords = {
        'nature': ['tree', 'flower', 'plant', 'landscape', 'mountain', 'water', 'sky', 'outdoor'],
        'people': ['person', 'people', 'human', 'face', 'portrait', 'group'],
        'animal': ['dog', 'cat', 'bird', 'animal', 'pet', 'wildlife'],
        'food': ['food', 'meal', 'cooking', 'restaurant', 'kitchen', 'eating'],
        'technology': ['computer', 'phone', 'device', 'screen', 'technology', 'digital'],
        'vehicle': ['car', 'truck', 'bike', 'plane', 'vehicle', 'transportation'],
        'building': ['building', 'house', 'architecture', 'structure', 'urban'],
        'art': ['painting', 'artwork', 'drawing', 'artistic', 'creative'],
        'sport': ['sport', 'game', 'playing', 'exercise', 'athletic'],
        'indoor': ['indoor', 'inside', 'room', 'interior'],
        'outdoor': ['outdoor', 'outside', 'exterior', 'landscape']
    }
    
    found_categories = []
    text_lower = text.lower()
    
    for category, keywords in category_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            found_categories.append(category)
    
    # Limit to 5 categories
    return found_categories[:5] if found_categories else ['general']

def extract_caption_from_text(text):
    """Extract a short caption from the analysis text"""
    sentences = text.split('.')
    if sentences:
        # Return the first meaningful sentence as caption
        for sentence in sentences:
            if len(sentence.strip()) > 10:
                return sentence.strip()[:100] + ("..." if len(sentence) > 100 else "")
    return "Image analysis"
