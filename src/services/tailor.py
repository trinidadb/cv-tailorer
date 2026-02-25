"""
CV Tailor Engine - Core functionality for resume tailoring
"""

from src.config.constants import ValidFileExtensions
from src.config.prompts import USER_PROMPT_TEMPLATE, USER_PROMPT_TEMPLATE_PRE_KEYWORD, SYSTEM_PROMPT_PRE_KEYWORD, SYSTEM_PROMPT
from src.llm import GeminiTailor

import sys
from src.config.schemas import TailoredResume
from src.llm import BaseLLMTailor
from src.utils import StructuredLaTeXConverter, UnstructuredLaTeXConverter, StructuredDocxConverter, save_tailored_resume


class CVTailor:

    def __init__(self, tailorer: BaseLLMTailor = None):
        self.tailorer = tailorer or GeminiTailor()
        print(f"\n{'='*60}")
        print("CV TAILOR INITIALIZED")
        print(f"{'='*60}\n")

    def tailor_resume(
        self,
        master_resume: str,
        job_description: str,
        structured_output: bool = True,
        generate_then_extract: bool = False,
        keywords: str = None
        # system_prompt: str = None, # if you want more user customization in the future
        # temperature: int = None,
        # max_tokens: int = None
    ) -> dict:

        print("📝 Tailoring your resume...")

        if keywords and structured_output:
            user_prompt = USER_PROMPT_TEMPLATE_PRE_KEYWORD.format(
                keywords_block=keywords,
                master_resume=master_resume,
                job_description=job_description
            )

            system_prompt = SYSTEM_PROMPT_PRE_KEYWORD

        else:
            user_prompt = USER_PROMPT_TEMPLATE.format(
                master_resume=master_resume,
                job_description=job_description
            )

            system_prompt = SYSTEM_PROMPT

        try:
            if structured_output:
                tailored_resume = self.tailorer.generate_then_extract_and_structure(system_prompt=system_prompt, user_prompt=user_prompt) if generate_then_extract else self.tailorer.generate_with_structured_output(system_prompt=system_prompt, user_prompt=user_prompt)
            else:
                tailored_resume = self.tailorer.generate(system_prompt=system_prompt, user_prompt=user_prompt)

            print("✓ Resume tailored successfully!\n")

            return tailored_resume

        except Exception as e:
            print(f"✗ Error during resume tailoring: {e}")
            raise

    # def generate_formated_cv(self, master_resume, job_description, save=True, generate_then_extract=False, structured_output=True, keywords=None, company_name=None, position_title=None, personal_info=None):
    #     keywords = keywords or []
    #     try:
    #         tailored_resume = self.tailor_resume(
    #             master_resume=master_resume,
    #             job_description=job_description,
    #             structured_output=structured_output,
    #             generate_then_extract=generate_then_extract,
    #             keywords=keywords
    #         )

    #         if isinstance(tailored_resume, TailoredResume):
    #             company_name = tailored_resume.company
    #             position_title = tailored_resume.position_title
    #             latex_output = StructuredLaTeXConverter().convert(tailored_resume, personal_info=personal_info)
    #             docx_output = StructuredDocxConverter().convert(tailored_resume, personal_info=personal_info)

    #         if save:
    #             _, timestamp = save_tailored_resume(latex_output, file_extension=ValidFileExtensions.LATEX, company_name=company_name, position_title=position_title)
    #             _, _ = save_tailored_resume(docx_output, file_extension=ValidFileExtensions.DOCX, company_name=company_name, position_title=position_title, timestamp=timestamp)


    #         print("\n" + "="*60)
    #         print("✓ SUCCESS!")
    #         print("="*60)
    #         print("="*60 + "\n")

    #         return latex_output, docx_output, company_name, position_title

    #     except Exception as e:
    #         print(f"\n✗ Error during tailoring: {e}")
    #         sys.exit(1)

    # def get_cv_with_unstructured_output_latex(self, master_resume, job_description, company_name=None, position_title=None):
    #     try:
    #         tailored_resume = self.tailor_resume(
    #             master_resume=master_resume,
    #             job_description=job_description,
    #             structured_output=False
    #         )

    #         # RESUME AS TEXT FOR COMPARISSON AS MANY TIMES UNSTRUCTURED LATEX CONVERTER FAILS
    #         _, timestamp = save_tailored_resume(tailored_resume, file_extension=ValidFileExtensions.TEXT, company_name=company_name, position_title=position_title)

    #         latex_output = UnstructuredLaTeXConverter().text_to_latex(tailored_resume)
    #         _, _ = save_tailored_resume(latex_output, file_extension=ValidFileExtensions.LATEX, company_name=company_name, position_title=position_title, timestamp=timestamp)

    #         print("\n" + "="*60)
    #         print("✓ SUCCESS!")
    #         print("="*60)
    #         print("\nNext steps:")
    #         print("1. Review the tailored resume")
    #         print("2. Make any personal adjustments")
    #         print("3. Convert to PDF (keep it text-selectable!)")
    #         print("4. Apply with confidence! 🚀")
    #         print("="*60 + "\n")

    #         return latex_output, company_name, position_title

    #     except Exception as e:
    #         print(f"\n✗ Error during tailoring: {e}")
    #         sys.exit(1)
