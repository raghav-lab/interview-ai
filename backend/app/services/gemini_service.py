import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_interview_questions(
    resume_text: str
):

    prompt = f"""
Analyze this resume and return ONLY valid JSON.

Format:

{{
  "candidate_role": "role name",
  "technical_questions": [],
  "project_questions": [],
  "hr_questions": []
}}

Generate:
- 10 technical questions
- 5 project questions
- 3 hr questions

Resume:

{resume_text}

Return JSON only.
"""

    response = model.generate_content(prompt)

    text = response.text

    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    return json.loads(text)