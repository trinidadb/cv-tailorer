from datetime import datetime
from pathlib import Path
import re
from src.config.constants import ValidFileExtensions


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


def save_tailored_resume(
    tailored_resume: str,
    file_extension: ValidFileExtensions = ValidFileExtensions.TEXT,
    output_dir: str = "./output",
    company_name: str = "Unknown",
    position_title: str = "Unknown",
    timestamp: str = None
) -> tuple:

    Path(output_dir).mkdir(parents=True, exist_ok=True) # Create output directory if it doesn't exist.

    timestamp = timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = sanitize_filename(f"tailored_{timestamp}_{company_name}_{position_title}")

    path = f"{output_dir}/{base_filename}{file_extension.value}"
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(tailored_resume)
        print(f"✓ Saved text resume to: {path}")
        return path, timestamp
    except Exception as e:
        print(f"✗ Error saving text file: {e}")