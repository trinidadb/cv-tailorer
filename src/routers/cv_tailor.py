from fastapi import UploadFile, File, Form, HTTPException
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import io

from src.tailor_resume import generate_tailored_cv_latex

router = APIRouter(
    prefix="/tailor",
    tags=["Tailor"],
    responses={404: {"description": "Not found"}},
)


@router.post("/generate")
async def tailor_resume(
    job_description: str = Form(...),
    resume_file: UploadFile = File(...),
):
    if not resume_file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only .txt resume files are supported.")

    try:
        # 2. Read the uploaded file content
        resume_content = await resume_file.read()
        master_resume = resume_content.decode("utf-8")

        #latex_content, company_name, position_title = generate_tailored_cv_latex(master_resume=master_resume, job_description=job_description, structured_output=True, save=False)

        mock_latex = r"""
            \documentclass{article}
            \begin{document}
            \section*{Tailored Resume}
            This is a MOCK response for frontend testing.
            \end{document}
            """
        
        latex_content = mock_latex
        company_name = "ZS"
        position_title = "Decision"

        stream = io.StringIO(latex_content)
        response = StreamingResponse(
            iter([stream.getvalue()]),
            media_type="application/x-tex"
        )
        response.headers["Content-Disposition"] = f"attachment; filename={company_name}_{position_title}.tex"

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during tailoring: {str(e)}")
