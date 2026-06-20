from sqlalchemy.orm import Session
from fastapi import Depends

from app.database.connection import get_db
from app.database.resume_model import Resume
from fastapi import APIRouter, UploadFile, File
import shutil
import os
import fitz

from app.utils.skill_extractor import extract_skills

router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    pdf = fitz.open(file_path)

    text = ""

    for page in pdf:
        text += page.get_text()

    pdf.close()

    skills = extract_skills(text)

    resume = Resume(
    filename=file.filename,
    resume_text=text,
    extracted_skills=",".join(skills),
    user_id=1
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {
    "message": "Resume uploaded successfully",
    "resume_id": resume.id,
    "filename": file.filename,
    "skills": skills,
    "preview": text[:500]
    }