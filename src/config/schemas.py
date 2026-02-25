from pydantic import BaseModel
from typing import Optional


# ------------------------------------------------------------------
# KEYWORD EXTRACTOR
# ------------------------------------------------------------------

class ExtractedKeyword(BaseModel):
    keyword: str
    category: str   # "technical" | "tool" | "soft_skill" | "management" | "domain"
    rank: int       # 1 = most important


class ExtractedKeywords(BaseModel):
    keywords: list[ExtractedKeyword]

    def top(self, n: int = 30) -> list[str]:
        sorted_kws = sorted(self.keywords, key=lambda k: k.rank)
        return [k.keyword for k in sorted_kws[:n]]

    def format_for_prompt(self, n: int = 30) -> str:
        top = sorted(self.keywords, key=lambda k: k.rank)[:n]
        lines = "\n".join(f"{kw.rank}. [{kw.category}] {kw.keyword}" for kw in top)
        return f"TOP {n} JD KEYWORDS (ranked by importance):\n{lines}"

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
    name: Optional[str] = "Your Name"
    email: Optional[str] = "youremail@example.com"
    linkedin: Optional[str] = "suffix"
    github: Optional[str] = "username"
    location: Optional[str] = "City, Country"


# ------------------------------------------------------------------
# ATS
# ------------------------------------------------------------------

class KeywordMatch(BaseModel):
    keyword: str
    tier: str           # "critical" | "important" | "nice_to_have"

class KeywordPartialMatch(BaseModel):
    keyword: str
    partial_match: str
    tier: str           # "critical" | "important" | "nice_to_have"

class KeywordMissing(BaseModel):
    keyword: str
    tier: str           # "critical" | "important" | "nice_to_have"


class ATSScoreReport(BaseModel):
    keyword_density: float              # percentage estimate
    keyword_matches: list[KeywordMatch]
    keyword_partial_matches: list[KeywordPartialMatch]
    keyword_missing: list[KeywordMissing]
    improvement_suggestions: list[str]  # ordered by impact
