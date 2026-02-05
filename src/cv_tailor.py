"""
CV Tailor Engine - Core functionality for resume tailoring
"""

from src.llm import GeminiClient
from config.constants import MAX_TOKENS
from config.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE


class CVTailor:
    """Main CV tailoring engine"""

    def __init__(self, preferred_provider: str = "anthropic"):
        """
        Initialize the CV Tailor

        Args:
            preferred_provider: "anthropic" or "gemini"
        """
        self.llm_client = GeminiClient()
        print(f"\n{'='*60}")
        print(f"CV TAILOR INITIALIZED")
        print(f"{'='*60}\n")

    def tailor_resume(
        self,
        master_resume: str,
        job_description: str,
        max_tokens: int = MAX_TOKENS
    ) -> str:
        """
        Tailor a resume to a specific job posting

        Args:
            master_resume: Your complete resume as text
            job_description: The job posting text
            max_tokens: Maximum length of response

        Returns:
            Tailored resume as text
        """
        # Validate inputs
        if not master_resume or not master_resume.strip():
            raise ValueError("Master resume cannot be empty")

        if not job_description or not job_description.strip():
            raise ValueError("Job description cannot be empty")

        # Prepare the user prompt
        user_prompt = USER_PROMPT_TEMPLATE.format(
            master_resume=master_resume,
            job_description=job_description
        )

        print("📝 Tailoring your resume...")
        print(f"   Master resume length: {len(master_resume)} characters")
        print(f"   Job description length: {len(job_description)} characters")
        print()

        # Generate tailored resume
        try:
            tailored_resume = self.llm_client.generate(user_prompt=user_prompt)

            print("✓ Resume tailored successfully!\n")
            return tailored_resume

        except Exception as e:
            print(f"✗ Error during resume tailoring: {e}")
            raise

    def save_tailored_resume(self, tailored_resume: str, output_path: str):
        """
        Save the tailored resume to a file

        Args:
            tailored_resume: The tailored resume text
            output_path: Where to save the file
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(tailored_resume)
            print(f"✓ Saved tailored resume to: {output_path}")
        except Exception as e:
            print(f"✗ Error saving file: {e}")
            raise


def load_text_file(file_path: str) -> str:
    """
    Load a text file

    Args:
        file_path: Path to the text file

    Returns:
        File contents as string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading file {file_path}: {e}")
