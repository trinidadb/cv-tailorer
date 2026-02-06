# cv-tailorer 🚀

**ATS-optimized CV customization without the subscription.**

`cv-tailorer` is an open-source MVP designed to help job seekers bypass rigid Applicant Tracking Systems (ATS). While most professional tailoring tools are behind paywalls, this project leverages the Gemini API to intelligently adapt your existing experience to specific job descriptions—maintaining authenticity while maximizing keyword relevance.

## 🌟 Key Philosophy
The core idea is to keep your new CV real but allow for logical creativity in customization. By focusing on how a machine (ATS) parses data and how a human (Recruiter) perceives value, the tool optimizes your existing background to pass filters and secure interviews.

## 🛠 Tech Stack
- **Language:** Python 3.x
- **LLM:** Google Gemini (Generative AI)
- **Environment Management:** `python-dotenv`
- **Output:** Clean Text (Optimized for LaTeX conversion)

## 🚀 Getting Started

### 1. Prerequisites
- A **Gemini API Key**. You can get one for free at [Google AI Studio](https://aistudio.google.com/).
- Python installed on your machine.

### 2. Installation
First, clone the repository and navigate to the project folder.

# Create and activate a virtual environment
```
python -m venv .venv

# Activate on Windows:
.venv\Scripts\activate
# Activate on macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory and add your API key:

```
GEMINI_API_KEY=your_api_key_here
```

## 📖 How to Use
The tool requires four main inputs to generate a tailored CV. Run the script using the following command:

```
python tailor_resume.py "data/your_master_resume.txt" "data/target_job_description.txt" "Company Name" "Position Title"
```

## ⚠️ Important Considerations
- **Scope:** This tool focuses exclusively on the high-impact, dynamic sections of a CV: **HEADLINE**, **PROFESSIONAL SUMMARY**, **PROFESSIONAL EXPERIENCE**, and **SKILLS**.
- **Static Sections:** It does **not** process Education, Certificates, or Personal Info. It is recommended to keep these sections static in your final LaTeX/Word template and only update the AI-generated sections.
- **Skills Input:** For best results, list your skills in your master resume as a "rough list" rather than grouping them. The LLM will intelligently categorize and select the most relevant ones for the specific JD.
- **Profile Input:** For best results, don't include a profile in the input CV. The tool will build it for you :D.
- **Prompt Logic:** This project uses `prompt_v3`, which is specifically tuned to:
    - Match Job Titles exactly.
    - Vary action verbs (e.g., swapping "Led" for "Spearheaded" or "Architected") to avoid keyword-stuffing penalties.
    - Ensure a consistent date format (`mm/YYYY`).
    - Enforce the "Action + Context + Result" bullet point structure.

## 🤝 Contributing
This is an MVP and is still being refined. If you find bugs or have ideas for better prompts, feel free to open an issue or a PR!

---
*Disclaimer: This tool is intended to assist in the presentation of your existing experience. Never use AI to fabricate qualifications or achievements.*