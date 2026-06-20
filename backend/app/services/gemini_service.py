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
You are a senior software engineer interviewer.

Analyze the resume below.

Generate:

1. Candidate Role
2. 10 Technical Questions
3. 5 Project Questions
4. 3 HR Questions

Resume:

{resume_text}
"""

    response = model.generate_content(
        prompt
    )

    return response.text