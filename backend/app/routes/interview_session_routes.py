from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.resume_model import Resume
from app.database.interview_model import Interview
from app.database.interview_question_model import InterviewQuestion

from app.security.auth import get_current_user

from app.services.gemini_service import (
    generate_interview_questions
)

router = APIRouter()


@router.post("/start-interview/{resume_id}")
def start_interview(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
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

    try:
        questions = generate_interview_questions(
            resume.resume_text
        )

        print("QUESTIONS:")
        print(questions)

    except Exception as e:
        print("START INTERVIEW ERROR:")
        print(e)
        raise e
    interview = Interview(
        user_id=current_user["user_id"],
        resume_id=resume_id
    )

    db.add(interview)
    db.commit()
    db.refresh(interview)

    all_questions = (
        questions["technical_questions"]
        + questions["project_questions"]
        + questions["hr_questions"]
    )

    for q in all_questions:

        question_record = InterviewQuestion(
            interview_id=interview.id,
            question=q,
            answer="",
            score=0,
            feedback=""
        )

        db.add(question_record)

    db.commit()

    return {
        "interview_id": interview.id,
        "total_questions": len(all_questions)
    }