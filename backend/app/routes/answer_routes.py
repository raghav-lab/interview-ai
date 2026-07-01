import json

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

    print("EVALUATION:", evaluation)

    try:
        question_record.answer = request.answer

        # Safely extract score
        score = evaluation.get("score", 0)

        if isinstance(score, str):
            # Extract digits if Gemini returns "8/10" or "Score: 8"
            digits = "".join(
                c for c in score if c.isdigit()
            )

            score = int(digits) if digits else 0

        question_record.score = int(score)

        question_record.feedback = json.dumps(
            evaluation
        )

        db.commit()

        print("Saved successfully")
        print("Answer:", question_record.answer)
        print("Score:", question_record.score)

    except Exception as e:
        db.rollback()
        print("DB ERROR:", e)

        return {
            "message": "Failed to save answer",
            "error": str(e)
        }

    return {
        "message": "Answer evaluated",
        "evaluation": evaluation
    }