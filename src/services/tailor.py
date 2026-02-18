"""
CV Tailor Engine - Core functionality for resume tailoring
"""

from src.config.constants import ValidFileExtensions
from src.config.prompts import USER_PROMPT_TEMPLATE
from src.llm import GeminiClient

import sys
from src.config.schemas import TailoredResume
from src.llm import BaseLLMClient
from src.utils import StructuredLaTeXConverter, UnstructuredLaTeXConverter, save_tailored_resume


class CVTailor:
    """Main CV tailoring engine"""

    def __init__(self, llm_client: BaseLLMClient = None):
        self.llm_client = llm_client or GeminiClient()
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

    def generate_tailored_cv_latex(self, master_resume, job_description, save=True, generate_then_extract=False, structured_output=True, company_name=None, position_title=None, personal_info=None):
        try:
            tailored_resume = self.tailor_resume(
                master_resume=master_resume,
                job_description=job_description,
                structured_output=structured_output,
                generate_then_extract=generate_then_extract
            )

            if isinstance(tailored_resume, TailoredResume):
                timestamp = None
                latex_output = StructuredLaTeXConverter().convert(tailored_resume, personal_info=personal_info)
                company_name = tailored_resume.company
                position_title = tailored_resume.position_title

            else:
                # RESUME AS TEXT FOR COMPARISSON AS MANY TIMES UNSTRUCTURED LATEX CONVERTER FAILS
                _, timestamp = save_tailored_resume(tailored_resume, file_extension=ValidFileExtensions.TEXT, company_name=company_name, position_title=position_title)
                latex_output = UnstructuredLaTeXConverter().text_to_latex(tailored_resume)

            if save:
                _, _ = save_tailored_resume(latex_output, file_extension=ValidFileExtensions.LATEX, company_name=company_name, position_title=position_title, timestamp=timestamp)

            print("\n" + "="*60)
            print("✓ SUCCESS!")
            print("="*60)
            print("\nNext steps:")
            print("1. Review the tailored resume")
            print("2. Make any personal adjustments")
            print("3. Convert to PDF (keep it text-selectable!)")
            print("4. Apply with confidence! 🚀")
            print("="*60 + "\n")

            return latex_output, company_name, position_title

        except Exception as e:
            print(f"\n✗ Error during tailoring: {e}")
            sys.exit(1)

