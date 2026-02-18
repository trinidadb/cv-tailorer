from fastapi import UploadFile, File, Form, HTTPException, Depends
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import io
from typing import Optional

from src.config.schemas import PersonalInfo
from src.dependencies import get_tailor
from src.utils import sanitize_filename

router = APIRouter(
    prefix="/tailor",
    tags=["Tailor"],
    responses={404: {"description": "Not found"}},
)


@router.post("/generate")
async def tailor_resume(
    job_description: str = Form(...),
    resume_file: UploadFile = File(...),
    name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    linkedin: Optional[str] = Form(None),
    github: Optional[str] = Form(None)
):
    if not resume_file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only .txt resume files are supported.")

    try:
        resume_content = await resume_file.read()
        master_resume = resume_content.decode("utf-8")

        personal_info = PersonalInfo(name=name, email=email, location=location, linkedin=linkedin, github=github)

        latex_content, company_name, position_title = get_tailor().generate_tailored_cv_latex(master_resume=master_resume, job_description=job_description, structured_output=True, save=False, personal_info=personal_info)

        # mock_latex = r"""
        #     \documentclass{article}
        #     \begin{document}
        #     \section*{Tailored Resume}
        #     This is a MOCK response for frontend testing.
        #     \end{document}
        #     """
        
        # latex_content = mock_latex
        # company_name = "ZS"
        # position_title = "Decision"

        filename = sanitize_filename(f"{company_name}_{position_title}")

        return StreamingResponse(
            io.BytesIO(latex_content.encode("utf-8")),
            media_type="application/x-tex",
            headers={"Content-Disposition": f"attachment; filename={filename}.tex"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during tailoring: {str(e)}")
