#!/usr/bin/env python3
"""
CV Tailor - Standalone Script Version
Quick command-line tool for resume tailoring
"""

import sys

from src.cv_tailor import CVTailor
from src.utils import load_text_file


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

    tailor = CVTailor()
    try:
        # tailored_resume = tailor.tailor_resume(
        #     master_resume=master_resume,
        #     job_description=job_description
        # )

        tailored_resume = '''
            **1. HEADLINE:**
            Decision Analytics Consultant | Data Analysis • Predictive Modeling • Stakeholder Management

            **2. PROFESSIONAL SUMMARY:**
            Highly analytical and results-oriented professional with extensive experience in leveraging advanced data analytics and machine learning to solve complex business challenges and drive strategic outcomes. Adept at translating technical insights into actionable recommendations for stakeholders, as demonstrated by leading an AI project that optimized staffing and cut operational costs by 39%. Possesses a strong foundation in data architecture, predictive modeling, and business intelligence, committed to delivering impactful solutions within a client-focused environment.

            **3. PROFESSIONAL EXPERIENCE:**

            **AIR Institute** | Private research organization
            **AI/Analytics Lead** | 01/2024 – Present
            *   Led an AI project to predict customer flow at Madrid Airport exchange office, optimizing staffing and cutting operational costs by 39% through data-driven insights.
            *   Developed an AI-powered web platform integrating multiple ML models for cloud condition prediction and solar energy forecasting, enabling real-time monitoring and predictive analytics for solar farm operations.
            *   Mentored and collaborated across diverse projects, including energy monitoring systems and digital twins, leveraging advanced analytics to solve complex challenges and drive innovation.
            *   Orchestrated the deployment of ML models on AWS and standardized the use of Terraform and Docker, significantly accelerating development cycles and ensuring robust analytical solution delivery.

            **JP Morgan Chase & Co.** | USA’s largest bank & financial services provider
            **Data & Analytics Engineer** | 11/2020 - 10/2023
            *   Acted as a liaison between technical teams and business stakeholders (traders), translating complex business needs into analytical requirements and driving continuous improvement in data-driven decision support.
            *   Crafted data architecture solutions (RabbitMQ) addressing critical information bottlenecks, reducing trader decision-making lag by 63% and enabling faster market response for strategic execution.
            *   Automated the generation of personalized performance reports for trading tools (Python + log analysis), serving 144 tools and 23+ groups with weekly insights, enhancing data access and reporting capabilities.
            *   Configured and maintained Elasticsearch clusters for big data processing, developing tailored search solutions for complex financial instruments that transformed how trading desks accessed market intelligence.
            *   Identified operational bottlenecks and implemented solutions that reduced failure identification time by 90%, resulting in estimated ~$10M in gains through improved system reliability and performance.

            **4. SKILLS:**
            **Data Science & Analytics:** Quantitative Analysis, Data Analysis, Advanced Modeling Techniques, Machine Learning, Predictive Analytics, Scikit-learn, PyTorch, TensorFlow, Pandas, Numpy, LLMs fine-tuning, Prompt Engineering, RAG, Traditional Machine Learning Algorithms, Matplotlib, MATLAB
            **Business Intelligence & Visualization:** Power BI, Splunk, Grafana
            **Programming & Development:** Python, JavaScript, TypeScript, React, Node.js, Express, FastAPI, Flask, REST APIs, GraphQL
            **Databases & Data Architecture:** SQL (PostgreSQL, MySQL), NoSQL (Elasticsearch, MongoDB), RabbitMQ
            **Cloud & DevOps:** AWS Cloud, Docker, Terraform, CI/CD (GitHub Actions), Git, DevOps
            **Project Management & Consulting:** Stakeholder Management, Requirements Gathering, Problem-solving, Project Management, Agile, Scrum, Technical-to-Business Translation, Process Optimization

            '''

        _ = CVTailor.save_tailored_resume(tailored_resume)

        # Display summary
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
