from fastapi import FastAPI

from app.database.connection import engine
from app.database.models import Base

from app.routes.user_routes import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)

@app.get("/")
def home():
    return {
        "message": "InterviewAI Backend Running"
    }