#!/usr/bin/env python3
"""
CV Tailor - Standalone Script Version
Quick command-line tool for resume tailoring
"""

import sys
from config.constants import ValidFileExtensions
from config.schemas import TailoredResume
from src.cv_tailor import CVTailor
from src.utils import load_text_file
from src.utils import StructuredLaTeXConverter, UnstructuredLaTeXConverter


def main():
    """Main function for standalone script usage"""

    print("\n" + "="*60)
    print("CV TAILOR - ATS-Optimized Resume Tailoring")
    print("="*60 + "\n")

    resume_file = sys.argv[1]
    job_file = sys.argv[2]
    company_name = sys.argv[3] if len(sys.argv) > 3 else "Unknown"
    position_title = sys.argv[4] if len(sys.argv) > 4 else "Unknown"

    try:
        print(f"📄 Loading resume from: {resume_file}")
        master_resume = load_text_file(resume_file)

        print(f"📄 Loading job description from: {job_file}")
        job_description = load_text_file(job_file)

    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        print("\nUsage: python tailor_resume.py <resume_file> <job_file>")
        sys.exit(1)

    tailor = CVTailor()
    try:
        tailored_resume = tailor.tailor_resume(
            master_resume=master_resume,
            job_description=job_description,
            generate_then_extract=True
        )

        # tailored_resume = load_text_file("output/tailored_20260207_202322_ZS_Data-Analyst.txt")

        if isinstance(tailored_resume, TailoredResume):
            timestamp = None
            latex_output = StructuredLaTeXConverter().convert(tailored_resume)

        else:
            # RESUME AS TEXT FOR COMPARISSON AS MANY TIMES UNSTRUCTURED LATEX CONVERTER FAILS
            _, timestamp = CVTailor.save_tailored_resume(tailored_resume, file_extension=ValidFileExtensions.TEXT, company_name=company_name, position_title=position_title)
            latex_output = UnstructuredLaTeXConverter().text_to_latex(tailored_resume)

        _, _ = CVTailor.save_tailored_resume(latex_output, file_extension=ValidFileExtensions.LATEX, company_name=company_name, position_title=position_title, timestamp=timestamp)

        print("\n" + "="*60)
        print("✓ SUCCESS!")
        print("="*60)
        print("\nNext steps:")
        print("1. Review the tailored resume")
        print("2. Make any personal adjustments")
        print("3. Convert to PDF (keep it text-selectable!)")
        print("4. Apply with confidence! 🚀")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\n✗ Error during tailoring: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
