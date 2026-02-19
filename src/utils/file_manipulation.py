from datetime import datetime
from docx.document import Document as DocumentObject
from pathlib import Path
import re

from src.config.constants import ValidFileExtensions


def _make_path(
    output_dir: str,
    company_name: str,
    position_title: str,
    file_extension: ValidFileExtensions,
    timestamp: str = None,
) -> tuple[str, str]:
    """Build output path and return (path, timestamp)."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    timestamp = timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")
    base = sanitize_filename(f"tailored_{timestamp}_{company_name}_{position_title}")
    path = f"{output_dir}/{base}{file_extension.value}"
    return path, timestamp


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
    tailored_resume: str | DocumentObject,
    file_extension: ValidFileExtensions = ValidFileExtensions.TEXT,
    output_dir: str = "./output",
    company_name: str = "Unknown",
    position_title: str = "Unknown",
    timestamp: str = None
) -> tuple:

    path, timestamp = _make_path(output_dir, company_name, position_title, file_extension, timestamp=timestamp)

    match file_extension:
        case ValidFileExtensions.TEXT | ValidFileExtensions.LATEX:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(tailored_resume)
                print(f"✓ Saved text resume to: {path}")
                return path, timestamp
            except Exception as e:
                print(f"✗ Error saving text file: {e}")

        case ValidFileExtensions.DOCX:
            try:
                tailored_resume.save(path)
                print(f"✔ Saved .docx to: {path}")
                return path, timestamp
            except Exception as e:
                print(f"✗ Error saving .docx: {e}")
                raise


def load_text_file(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading file {file_path}: {e}")