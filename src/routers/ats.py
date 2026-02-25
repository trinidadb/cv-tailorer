from fastapi import Form, HTTPException
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List
from pydantic import TypeAdapter

from src.config.constants import ValidModels
from src.config.schemas import KeywordMatch, KeywordMissing, KeywordPartialMatch
from src.dependencies import get_ats
from src.services.cache import get as get_from_cache

router = APIRouter(
    prefix="/ats",
    tags=["ATS"],
    responses={404: {"description": "Not found"}},
)


@router.post("/score")
async def score(
    resume_id: str,
    job_description: str = Form(...),
    model: ValidModels = Form(ValidModels.GEM_25_FLASH),
):
    try:
        tailored_resume = get_from_cache(resume_id)
        report = get_ats(model=model).score(tailored_resume, job_description)

        return JSONResponse({"keyword_density": report.keyword_density,
                             "keyword_matches": TypeAdapter(List[KeywordMatch]).dump_python(report.keyword_matches),
                             "keyword_partial_matches": TypeAdapter(List[KeywordPartialMatch]).dump_python(report.keyword_partial_matches),
                             "keyword_missing": TypeAdapter(List[KeywordMissing]).dump_python(report.keyword_missing),
                             "improvement_suggestions": report.improvement_suggestions,
                             })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during tailoring: {str(e)}")
