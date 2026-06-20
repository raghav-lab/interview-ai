from app.services.gemini_service import generate_interview_questions

result = generate_interview_questions(
    "Python React FastAPI PostgreSQL"
)

print(type(result))
print(result["candidate_role"])