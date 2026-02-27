from fastapi import UploadFile, File, Form, HTTPException, Query
from fastapi import APIRouter
from fastapi.responses import StreamingResponse, JSONResponse
import io
from typing import Optional

from src.config.constants import ValidModels, ValidProviders, ANTHROPIC_TEMPERATURE, GEMINI_TEMPERATURE
from src.config.schemas import PersonalInfo
from src.dependencies import get_tailor, get_client_provider, MODELS
from src.services.cache import store, get
from src.utils import StructuredLaTeXConverter, StructuredDocxConverter, sanitize_filename

router = APIRouter(
    prefix="/tailor",
    tags=["Tailor"],
    responses={404: {"description": "Not found"}},
)


@router.post("/generate")
async def tailor_resume(
    job_description: str = Form(...),
    resume_file: UploadFile = File(...),
    first_extract_keywords: bool = Form(...),
    keywords_model: ValidModels = Form(ValidModels.GEM_25_FLASH),
    tailorer_model: ValidModels = Form(ValidModels.GEM_25_FLASH),
    temperature: Optional[float] = Form(None, ge=0.0, le=1.0) # [0-1]
):
    if not resume_file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only .txt resume files are supported.")

    try:
        resume_content = await resume_file.read()
        master_resume = resume_content.decode("utf-8")
        is_gemini_provider = tailorer_model in MODELS[ValidProviders.GEMINI]
        if temperature and is_gemini_provider:
            temperature = temperature*2  # Gemini temperature range in between 0 and 2

        if not temperature:
            temperature = GEMINI_TEMPERATURE if is_gemini_provider else ANTHROPIC_TEMPERATURE

        if first_extract_keywords:
            extracted_keywords = get_client_provider(model=keywords_model).get_keywords(job_description=job_description, top_n=30)
            top_extracted_keywords = extracted_keywords.top()
            tailored_resume = get_tailor(model=tailorer_model).tailor_resume(master_resume=master_resume, job_description=job_description, structured_output=True, keywords=extracted_keywords.format_for_prompt(), temperature=temperature)

        else:
            top_extracted_keywords = "not_available"
            tailored_resume = get_tailor(model=tailorer_model).tailor_resume(master_resume=master_resume, job_description=job_description, structured_output=True, temperature=temperature)

        tailored_resume_id = store(tailored_resume)

        return JSONResponse({"resume_id": tailored_resume_id,
                             "keywords": top_extracted_keywords})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during tailoring: {str(e)}")


def _prepare_for_format(resume_id, name, email, location, linkedin, github):
    tailored_resume = get(resume_id)

    if not tailored_resume:
        raise HTTPException(
            status_code=404,
            detail=f"Error generating tailored resumen. Resume not generated."
        )

    personal_info = PersonalInfo(name=name, email=email, location=location, linkedin=linkedin, github=github)
    filename = sanitize_filename(f"{tailored_resume.company}_{tailored_resume.position_title}")

    return tailored_resume, personal_info, filename


@router.get("/{resume_id}/latex")
async def get_latex(
    resume_id: str,
    name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    linkedin: Optional[str] = Query(None),
    github: Optional[str] = Query(None)
):
    try:
        tailored_resume, personal_info, filename = _prepare_for_format(resume_id, name, email, location, linkedin, github)
        latex_content = StructuredLaTeXConverter().convert(tailored_resume, personal_info=personal_info)

        return StreamingResponse(
            io.BytesIO(latex_content.encode("utf-8")),
            media_type="application/x-tex",
            headers={"Content-Disposition": f"attachment; filename={filename}.tex"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during tailoring: {str(e)}")


@router.get("/{resume_id}/docx")
async def get_docx(
    resume_id: str,
    name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    linkedin: Optional[str] = Query(None),
    github: Optional[str] = Query(None)
):
    try:
        tailored_resume, personal_info, filename = _prepare_for_format(resume_id, name, email, location, linkedin, github)
        docx_document = StructuredDocxConverter().convert(tailored_resume, personal_info=personal_info)

        docx_buffer = io.BytesIO()
        docx_document.save(docx_buffer)
        docx_buffer.seek(0)

        return StreamingResponse(
            docx_buffer,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={filename}.docx"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during tailoring: {str(e)}")
