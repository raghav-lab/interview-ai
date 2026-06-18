from fastapi import FastAPI

from app.database.connection import engine
from app.database.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "InterviewAI Backend Running"
    }