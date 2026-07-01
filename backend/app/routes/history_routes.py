from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.interview_model import Interview
from app.database.interview_question_model import InterviewQuestion

from app.security.auth import get_current_user

router = APIRouter()


@router.get("/interviews")
def get_interviews(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    interviews = db.query(
        Interview
    ).filter(
        Interview.user_id ==
        current_user["user_id"]
    ).all()

    results = []

    for interview in interviews:

        questions = db.query(
            InterviewQuestion
        ).filter(
            InterviewQuestion.interview_id == interview.id
        ).all()

        answered = [
            q for q in questions
            if q.answer and q.answer.strip()
        ]

        avg_score = 0

        if answered:
            avg_score = round(
                sum(q.score for q in answered)
                / len(answered),
                2
            )

        results.append({
            "interview_id": interview.id,
            "resume_id": interview.resume_id,
            "questions_answered": len(answered),
            "average_score": avg_score
        })

    return results