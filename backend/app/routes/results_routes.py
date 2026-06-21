from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.connection import get_db
from app.database.interview_question_model import InterviewQuestion

router = APIRouter()


@router.get("/interview/{interview_id}/results")
def interview_results(
    interview_id: int,
    db: Session = Depends(get_db)
):

    questions = db.query(
        InterviewQuestion
    ).filter(
        InterviewQuestion.interview_id == interview_id
    ).all()

    if not questions:
        return {
            "message": "Interview not found"
        }

    total_questions = len(questions)

    answered_questions = sum(
        1 for q in questions
        if q.answer and q.answer.strip()
    )

    total_score = sum(
        q.score for q in questions
    )

    average_score = (
        total_score / answered_questions
        if answered_questions > 0
        else 0
    )

    overall_score = round(
        average_score * 10,
        2
    )

    return {
        "interview_id": interview_id,
        "questions_total": total_questions,
        "questions_answered": answered_questions,
        "average_score": round(
            average_score,
            2
        ),
        "overall_score": overall_score
    }