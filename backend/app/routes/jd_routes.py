from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.resume_model import Resume
from app.security.auth import get_current_user

from app.utils.skill_extractor import extract_skills

router = APIRouter()


class JDRequest(BaseModel):
    resume_id: int
    job_description: str


@router.post("/match-jd")
def match_jd(
    request: JDRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # Get resume from DB
    resume = db.query(Resume).filter(
        Resume.id == request.resume_id,
        Resume.user_id == current_user["user_id"]
    ).first()

    if not resume:
        return {
            "message": "Resume not found"
        }

    # Resume skills
    resume_skills = [
        skill.strip().lower()
        for skill in resume.extracted_skills.split(",")
    ]

    # JD skills
    jd_skills = [
        skill.lower()
        for skill in extract_skills(
            request.job_description
        )
    ]

    # Matching skills
    matching_skills = [
        skill
        for skill in jd_skills
        if skill in resume_skills
    ]

    # Missing skills
    missing_skills = [
        skill
        for skill in jd_skills
        if skill not in resume_skills
    ]

    # Match score
    if len(jd_skills) > 0:
        match_score = round(
            len(matching_skills)
            / len(jd_skills) * 100
        )
    else:
        match_score = 0

    # Recommendations
    recommendations = [
        f"Learn {skill}"
        for skill in missing_skills
    ]

    return {
        "match_score": match_score,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "recommendations": recommendations
    }