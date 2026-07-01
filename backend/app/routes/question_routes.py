from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.interview_question_model import InterviewQuestion

router = APIRouter()


@router.get("/interview/{interview_id}/questions")
def get_questions(
    interview_id: int,
    db: Session = Depends(get_db)
):

    questions = db.query(
        InterviewQuestion
    ).filter(
        InterviewQuestion.interview_id == interview_id
    ).all()

    return questions