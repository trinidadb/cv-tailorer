"""
CV Tailor - Standalone Script Version
Quick command-line tool for resume tailoring
"""
import sys
from src.utils import load_text_file
from src.services.tailor import CVTailor

if __name__ == "__main__":
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

    CVTailor().generate_tailored_cv_latex(master_resume, job_description, save=True)
