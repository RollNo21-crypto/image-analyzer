from components.gemini_client import summarize_with_gemini

def categorize_content(content: str):
    prompt = f"""Analyze and categorize the following content into relevant themes like health, tech, finance, etc.

Content:
{content}

Return only a comma-separated list of 3–5 keywords."""
    return [c.strip().lower() for c in summarize_with_gemini(prompt).split(",")]
