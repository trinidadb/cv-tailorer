#!/usr/bin/env python3
"""
CV Tailor - Standalone Script Version
Quick command-line tool for resume tailoring
"""

import sys

from src.cv_tailor import CVTailor
from src.utils import load_text_file
from src.utils.latex_converter import LaTeXConverter


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
        )

        _ = CVTailor.save_tailored_resume(tailored_resume, company_name=company_name, position_title=position_title)

        latex_output = LaTeXConverter().text_to_latex(tailored_resume)

        with open("output/tailored_cv.tex", "w") as f:
            f.write(latex_output)

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
