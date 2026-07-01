import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


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

    try:
        response = model.generate_content(prompt)

        text = response.text

        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        return json.loads(text)

    except Exception as e:

        print("GEMINI ERROR:", e)

        return {
            "candidate_role": "Software Engineer",

            "technical_questions": [
                "Explain the four pillars of OOP.",
                "What is React useEffect?",
                "Explain REST APIs.",
                "What is normalization in DBMS?",
                "Explain OSI model.",
                "Explain multithreading in Java.",
                "What is JWT authentication?",
                "Explain indexing in databases.",
                "What is Docker?",
                "Difference between SQL and NoSQL."
            ],

            "project_questions": [
                "Explain your major project.",
                "What challenges did you face?",
                "How did you optimize performance?",
                "How did you design the database?",
                "What would you improve in the future?"
            ],

            "hr_questions": [
                "Tell me about yourself.",
                "Why should we hire you?",
                "Where do you see yourself in 5 years?"
            ]
        }

   