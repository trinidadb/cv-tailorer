"""
CV Tailor Engine - Core functionality for resume tailoring
"""
from datetime import datetime
from pathlib import Path

from src.llm import GeminiClient
from config.constants import ValidFileExtensions
from config.prompts import USER_PROMPT_TEMPLATE


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
        output_dir: str = "output",
        company_name: str = "Unknown",
        position_title: str = "Unknown"
    ) -> str:

        Path(output_dir).mkdir(parents=True, exist_ok=True) # Create output directory if it doesn't exist.

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"tailored_{timestamp}_{company_name}_{position_title}"

        match file_extension:

            case ValidFileExtensions.TEXT:
                path = f"{output_dir}/{base_filename}{file_extension.value}"      
                try:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(tailored_resume)
                    print(f"✓ Saved text resume to: {path}")
                    return path
                except Exception as e:
                    print(f"✗ Error saving text file: {e}")
