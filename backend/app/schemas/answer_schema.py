from pydantic import BaseModel

class AnswerSubmission(BaseModel):
    question_id: int
    answer: str