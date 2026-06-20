from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.interview_question_model import InterviewQuestion

from app.schemas.answer_schema import AnswerSubmission

from app.services.evaluation_service import (
    evaluate_answer
)

router = APIRouter()


@router.post("/submit-answer")
def submit_answer(
    request: AnswerSubmission,
    db: Session = Depends(get_db)
):

    question_record = db.query(
        InterviewQuestion
    ).filter(
        InterviewQuestion.id == request.question_id
    ).first()

    if not question_record:
        return {
            "message": "Question not found"
        }

    evaluation = evaluate_answer(
        question_record.question,
        request.answer
    )

    question_record.answer = request.answer
    question_record.feedback = evaluation

    db.commit()

    return {
        "message": "Answer evaluated",
        "evaluation": evaluation
    }