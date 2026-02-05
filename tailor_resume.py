#!/usr/bin/env python3
"""
CV Tailor - Standalone Script Version
Quick command-line tool for resume tailoring
"""

import sys
import os
from pathlib import Path
from datetime import datetime

from src.cv_tailor import CVTailor, load_text_file


def main():
    """Main function for standalone script usage"""

    print("\n" + "="*60)
    print("CV TAILOR - ATS-Optimized Resume Tailoring")
    print("="*60 + "\n")

    resume_file = sys.argv[1]
    job_file = sys.argv[2]

    try:
        print(f"📄 Loading resume from: {resume_file}")
        master_resume = load_text_file(resume_file)

        print(f"📄 Loading job description from: {job_file}")
        job_description = load_text_file(job_file)

    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        print("\nUsage: python tailor_resume.py <resume_file> <job_file>")
        sys.exit(1)

    # Initialize CV Tailor
    print("\n" + "-"*60)
    tailor = CVTailor(preferred_provider="anthropic")
    print("-"*60 + "\n")

    # Tailor the resume
    try:
        tailored_resume = tailor.tailor_resume(
            master_resume=master_resume,
            job_description=job_description
        )

        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"data/tailored_resume_{timestamp}.txt"

        # Save the result
        tailor.save_tailored_resume(tailored_resume, output_file)

        # Display summary
        print("\n" + "="*60)
        print("✓ SUCCESS!")
        print("="*60)
        print(f"Tailored resume saved to: {output_file}")
        print("\nNext steps:")
        print("1. Review the tailored resume")
        print("2. Make any personal adjustments")
        print("3. Convert to PDF (keep it text-selectable!)")
        print("4. Apply with confidence! 🚀")
        print("="*60 + "\n")

        # Ask if user wants to see the output
        show_output = input("Would you like to see the tailored resume now? (y/n): ").strip().lower()
        if show_output == 'y':
            print("\n" + "="*60)
            print("TAILORED RESUME")
            print("="*60 + "\n")
            print(tailored_resume)
            print("\n" + "="*60 + "\n")

    except Exception as e:
        print(f"\n✗ Error during tailoring: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
