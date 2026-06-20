from fastapi import APIRouter
from pydantic import BaseModel

from app.services.evaluation_service import evaluate_answer

router = APIRouter()


class AnswerRequest(BaseModel):
    question: str
    answer: str


@router.post("/evaluate-answer")
def evaluate(request: AnswerRequest):

    result = evaluate_answer(
        request.question,
        request.answer
    )

    return {
        "evaluation": result
    }