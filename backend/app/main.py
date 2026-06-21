from app.routes.interview_routes import router as interview_router
from app.routes.ai_routes import router as ai_router
from fastapi import FastAPI
from app.database.resume_model import Resume
from app.database.interview_model import Interview
from app.database.interview_question_model import InterviewQuestion

from app.database.connection import engine
from app.database.models import Base

from app.routes.user_routes import router as user_router
from app.routes.resume_routes import router as resume_router
from app.routes.interview_session_routes import (
    router as interview_session_router
)
from app.routes.answer_routes import (
    router as answer_router
)
from app.routes.results_routes import (
    router as results_router
)
from app.routes.jd_routes import router as jd_router
from fastapi.middleware.cors import CORSMiddleware
from app.routes.history_routes import (
    router as history_router
)
from app.routes.analysis_routes import (
    router as analysis_router
)
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai_router)
app.include_router(user_router)
app.include_router(resume_router)
app.include_router(interview_router)
app.include_router(interview_session_router)
app.include_router(answer_router)
app.include_router(results_router)
app.include_router(jd_router)
app.include_router(history_router)
app.include_router(analysis_router)

@app.get("/")
def home():
    return {
        "message": "InterviewAI Backend Running"
    }