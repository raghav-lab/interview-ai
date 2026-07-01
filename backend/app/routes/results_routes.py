from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.interview_model import Interview
from app.database.interview_question_model import InterviewQuestion

from app.security.auth import get_current_user

router = APIRouter()


@router.get("/interview/{interview_id}/results")
def get_results(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # Check whether interview exists
    interview = db.query(Interview).filter(
        Interview.id == interview_id
    ).first()

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    # Security check
    if interview.user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized access"
        )

    # Get all questions for this interview
    questions = db.query(InterviewQuestion).filter(
        InterviewQuestion.interview_id == interview_id
    ).all()

    total_questions = len(questions)

    answered_questions = [
        q for q in questions
        if q.answer and q.answer.strip()
    ]

    questions_answered = len(answered_questions)

    # Calculate average score
    if questions_answered > 0:
        average_score = round(
            sum(q.score for q in answered_questions)
            / questions_answered,
            2
        )
    else:
        average_score = 0

    # Overall percentage
    overall_score = round(
        (average_score / 10) * 100,
        2
    )

    return {
        "interview_id": interview.id,
        "questions_total": total_questions,
        "questions_answered": questions_answered,
        "average_score": average_score,
        "overall_score": overall_score
    }
