from app.services.gemini_service import model

def evaluate_answer(question: str, answer: str):

    prompt = f"""
You are a senior technical interviewer.

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer.

Return:
1. Score out of 10
2. Strengths
3. Weaknesses
4. Improved Answer

Keep the response structured.
"""

    response = model.generate_content(prompt)

    return response.text