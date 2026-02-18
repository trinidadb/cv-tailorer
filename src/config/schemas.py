from pydantic import BaseModel
from typing import Optional


# ------------------------------------------------------------------
# TAILORER
# ------------------------------------------------------------------

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


# ------------------------------------------------------------------
# ATS
# ------------------------------------------------------------------

class KeywordMatch(BaseModel):
    keyword: str
    tier: str           # "critical" | "important" | "nice_to_have"
    found: bool
    context: str        # where it was found, or suggestion if missing


class SectionScore(BaseModel):
    section: str        # "headline" | "summary" | "experience" | "skills"
    score: int          # 0-100
    feedback: str


class ATSScoreReport(BaseModel):
    overall_score: int                  # 0-100
    keyword_density: float              # percentage estimate
    keyword_matches: list[KeywordMatch]
    section_scores: list[SectionScore]
    missing_critical_keywords: list[str]
    improvement_suggestions: list[str]  # ordered by impact
    ats_verdict: str                    # "Strong Pass" | "Likely Pass" | "Borderline" | "Likely Fail"
