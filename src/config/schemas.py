from pydantic import BaseModel
from typing import Optional


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
    company: str
    position_title: str
    headline: str
    professional_summary: str
    professional_experience: list[ExperienceEntry]
    skills: list[SkillEntry]


class PersonalInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    location: Optional[str] = None
