import json

from app.services.gemini_service import model


def evaluate_answer(question: str, answer: str):

    prompt = f"""
You are a senior technical interviewer.

Question:
{question}

Candidate Answer:
{answer}

Return ONLY valid JSON.

Format:

{{
  "score": 0,
  "strengths": [],
  "weaknesses": [],
  "improved_answer": ""
}}

Rules:
- score must be between 0 and 10
- strengths should be a list
- weaknesses should be a list
- improved_answer should be a better version of the answer

Return JSON only.
"""

    response = model.generate_content(
        prompt
    )

    text = response.text

    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    return json.loads(text)