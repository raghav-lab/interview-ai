import json

from app.services.gemini_service import model


def match_resume_with_jd(
    resume_text: str,
    job_description: str
):

    prompt = f"""
Compare the resume with the job description.

Return ONLY JSON.

Format:

{{
  "match_score": 0,
  "matching_skills": [],
  "missing_skills": [],
  "recommendations": []
}}

Resume:
{resume_text}

Job Description:
{job_description}
"""

    response = model.generate_content(prompt)

    text = response.text
    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    return json.loads(text)