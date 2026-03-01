from fastapi import Form, HTTPException
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import TypeAdapter
from src.config.constants import ValidKeyExtractorMethods, ValidModels, ValidLanguages
from src.config.schemas import ExtractedKeyword
from src.dependencies import get_client_provider
from src.services.keywords import KeywordsExtractor


router = APIRouter(
    prefix="/keywords",
    tags=["Keywords - WIP - poor performance"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def get_keywords(
    job_description: str = Form(...),
    method:  ValidKeyExtractorMethods = Form(ValidKeyExtractorMethods.RANK_TF_IDF),
    top_n: Optional[int] = Form(30)
):
    try:

        extracted_keywords = KeywordsExtractor.get(job_description, method, top_n=top_n)

        return JSONResponse({"keywords": extracted_keywords})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during tailoring: {str(e)}")


@router.post("/llm")
async def get_keywords_using_llm(
    job_description: str = Form(...),
    top_n: Optional[int] = Form(30),
    model: ValidModels = Form(ValidModels.GEM_25_FLASH),
    language: ValidLanguages = Form(ValidLanguages.EN),
):
    try:

        extracted_keywords = get_client_provider(model=model).get_keywords(job_description=job_description, top_n=top_n, language=language)

        return JSONResponse({"keywords": TypeAdapter(List[ExtractedKeyword]).dump_python(extracted_keywords.keywords) })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during tailoring: {str(e)}")

