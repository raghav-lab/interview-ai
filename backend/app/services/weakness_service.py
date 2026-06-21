import json

from app.services.gemini_service import model


def analyze_weaknesses(feedbacks: list):

    prompt = f"""
You are an expert interview coach.

Analyze these interview feedbacks.

Feedbacks:
{feedbacks}

Return ONLY valid JSON.

Format:

{{
    "weak_topics": [],
    "strong_topics": [],
    "recommended_topics": [],
    "learning_plan": []
}}
"""

    response = model.generate_content(prompt)

    text = response.text

    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    try:
        return json.loads(text)

    except Exception as e:
        print("Gemini returned invalid JSON:")
        print(text)

        return {
            "weak_topics": ["Unable to analyze"],
            "strong_topics": [],
            "recommended_topics": [],
            "learning_plan": []
        }