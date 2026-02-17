from pydantic import BaseModel

class ExperienceEntry(BaseModel):
    job_title: str
    company: str
    location: str
    start_date: str  # mm/YYYY
    end_date: str    # mm/YYYY or "Present"
    tasks: list[str]

class SkillEntry(BaseModel):
    category_name: str
    skills: list[str]

class TailoredResume(BaseModel):
    headline: str
    professional_summary: str
    professional_experience: list[ExperienceEntry]
    skills: list[SkillEntry]
