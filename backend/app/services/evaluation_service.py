import json
from app.services.gemini_service import model


def evaluate_answer(question: str, answer: str):

    prompt = f"""
You are an interview evaluator.

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer in SIMPLE language.

Return ONLY JSON in this format:

{{
    "score": number between 1 and 10,
    "strengths": [
        "short point",
        "short point"
    ],
    "weaknesses": [
        "short point",
        "short point"
    ],
    "improvement_tip": "one sentence improvement tip",
    "improved_answer": "short ideal answer in 4-5 lines"
}}

Rules:
- Keep strengths and weaknesses very short.
- Maximum 3 strengths.
- Maximum 3 weaknesses.
- Use beginner-friendly language.
- Do not write long paragraphs.
"""

    try:

        response = model.generate_content(prompt)

        text = response.text.strip()

        print("RAW GEMINI RESPONSE:")
        print(text)

        # Remove markdown if present
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        result = json.loads(text)

        print("PARSED RESULT:")
        print(result)

        return result

    except Exception as e:

        print("Gemini Error:", e)

        # Fallback score based on answer length
        score = min(
            max(len(answer.split()) // 5, 1),
            10
        )

        return {
            "score": score,

            "strengths": [
                "Answer submitted successfully."
            ],

            "weaknesses": [
                "AI evaluation temporarily unavailable."
            ],

            "improved_answer":
                "Try adding more technical details, examples, and explanations to improve your answer."
    }