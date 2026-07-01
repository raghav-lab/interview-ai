from sqlalchemy.orm import Session
from fastapi import Depends

from app.database.connection import get_db
from app.database.resume_model import Resume
from fastapi import APIRouter, UploadFile, File

from app.security.auth import get_current_user

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
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
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
        user_id=current_user["user_id"]
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
@router.get("/resumes")
def get_resumes(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    resumes = db.query(Resume).filter(
        Resume.user_id == current_user["user_id"]
    ).all()

    return [
        {
            "id": resume.id,
            "filename": resume.filename,
            "skills": resume.extracted_skills
        }
        for resume in resumes
    ]
@router.get("/resumes")
def get_resumes(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    resumes = db.query(Resume).filter(
        Resume.user_id == current_user["user_id"]
    ).all()

    return [
        {
            "id": resume.id,
            "filename": resume.filename,
            "skills": resume.extracted_skills
        }
        for resume in resumes
    ]