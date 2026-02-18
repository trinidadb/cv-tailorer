"""
CV Tailor Engine - Core functionality for resume tailoring
"""
from datetime import datetime
from pathlib import Path

from src.config.constants import ValidFileExtensions
from src.config.prompts import USER_PROMPT_TEMPLATE
from src.llm import GeminiClient
from src.utils import sanitize_filename


class CVTailor:
    """Main CV tailoring engine"""

    def __init__(self):
        self.llm_client = GeminiClient()
        print(f"\n{'='*60}")
        print(f"CV TAILOR INITIALIZED")
        print(f"Provider: GEMINI")
        print(f"{'='*60}\n")

    def tailor_resume(
        self,
        master_resume: str,
        job_description: str,
        structured_output: bool = True,
        generate_then_extract: bool = False,
        # system_prompt: str = None, # if you want more user customization in the future
        # temperature: int = None,
        # max_tokens: int = None
    ) -> dict:

        user_prompt = USER_PROMPT_TEMPLATE.format(
            master_resume=master_resume,
            job_description=job_description
        )

        print("📝 Tailoring your resume...")
        print(f"   Master resume length: {len(master_resume)} characters")
        print(f"   Job description length: {len(job_description)} characters")
        print()

        try:
            if structured_output:
                tailored_resume = self.llm_client.generate_then_extract_and_structure(user_prompt=user_prompt) if generate_then_extract else self.llm_client.generate_with_structured_output(user_prompt=user_prompt)
            else:
                tailored_resume = self.llm_client.generate(user_prompt=user_prompt)

            print("✓ Resume tailored successfully!\n")

            return tailored_resume

        except Exception as e:
            print(f"✗ Error during resume tailoring: {e}")
            raise


    @staticmethod
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