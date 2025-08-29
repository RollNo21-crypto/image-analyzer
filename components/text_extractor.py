import requests
from bs4 import BeautifulSoup
from components.gemini_client import summarize_with_gemini

def extract_summary_from_link(link: str) -> str:
    try:
        html = requests.get(link, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        return summarize_with_gemini(f"Summarize this page:\n{text[:5000]}")
    except Exception as e:
        return f"Error fetching link: {e}"
