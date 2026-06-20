from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.resume_model import Resume

from app.services.gemini_service import (
    generate_interview_questions
)

router = APIRouter()


@router.get("/generate-questions/{resume_id}")
def generate_questions(
    resume_id: int,
    db: Session = Depends(get_db)
):

    resume = db.query(
        Resume
    ).filter(
        Resume.id == resume_id
    ).first()

    if not resume:

        return {
            "message": "Resume not found"
        }

    result = generate_interview_questions(
        resume.resume_text
    )

    return {
        "resume_id": resume_id,
        "questions": result
    }