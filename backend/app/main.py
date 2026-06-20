from app.routes.ai_routes import router as ai_router
from fastapi import FastAPI
from app.database.resume_model import Resume

from app.database.connection import engine
from app.database.models import Base

from app.routes.user_routes import router as user_router
from app.routes.resume_routes import router as resume_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(ai_router)
app.include_router(user_router)
app.include_router(resume_router)

@app.get("/")
def home():
    return {
        "message": "InterviewAI Backend Running"
    }