import re

def sanitize_filename(text: str) -> str:
    """
    Sanitize text for use in filename
    """
    text = re.sub(r'[^\w\s-]', '', text)  # Remove special characters, keep alphanumeric, spaces, and hyphens
    text = re.sub(r'\s+', '-', text)  # Replace spaces with hyphens
    text = re.sub(r'-+', '-', text)  # Remove consecutive hyphens
    text = text[:50]  # Limit length
    text = text.strip('-')  # Remove leading/trailing hyphens
    return text