"""
ATS Simulation Scorer
Evaluates a tailored resume against a job description, simulating ATS scoring logic.
Designed to work as a third step after generate → extract structured flow.
"""

from src.config.schemas import ATSScoreReport, TailoredResume
from src.llm import GeminiATS, BaseLLMATS


def _resume_to_text(resume) -> str:
    """
    Convert a TailoredResume Pydantic object to plain text for the scorer prompt.
    Keeps it readable so the LLM can assess keyword density naturally.
    """
    lines = [
        f"HEADLINE: {resume.headline}",
        "",
        f"PROFESSIONAL SUMMARY:\n{resume.professional_summary}",
        "",
        "PROFESSIONAL EXPERIENCE:",
    ]
    for entry in resume.professional_experience:
        lines.append(f"{entry.job_title} | {entry.company} | {entry.location} | {entry.start_date} - {entry.end_date}")
        for task in entry.tasks:
            lines.append(f"  - {task}")
        lines.append("")

    lines.append("SKILLS:")
    for skill_entry in resume.skills:
        skills_str = ", ".join(skill_entry.skills)
        lines.append(f"  {skill_entry.category_name}: {skills_str}")

    return "\n".join(lines)


class ATSSystem:

    def __init__(self, ats: BaseLLMATS = None):
        self.ats = ats or GeminiATS()

    def score(self, resume: TailoredResume, job_description: str) -> ATSScoreReport:
        resume_text = _resume_to_text(resume)
        return self.ats.score(resume_text=resume_text, job_description=job_description)
