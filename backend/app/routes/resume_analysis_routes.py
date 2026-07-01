from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.resume_model import Resume
from app.security.auth import get_current_user

router = APIRouter()


@router.get("/resume-analysis/{resume_id}")
def analyze_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    resume = db.query(Resume).filter(
        Resume.id == resume_id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    if resume.user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized"
        )

    text = resume.resume_text.lower()

    score = 50

    strengths = []
    weaknesses = []
    suggestions = []

    # Skills check
    skills_count = len(
        resume.extracted_skills.split(",")
    )

    if skills_count >= 8:
        score += 15
        strengths.append(
            "Strong technical skill set"
        )
    else:
        weaknesses.append(
            "Limited technical skills detected"
        )
        suggestions.append(
            "Add more relevant technical skills"
        )

    # Projects
    if "project" in text:
        score += 10
        strengths.append(
            "Projects section present"
        )
    else:
        weaknesses.append(
            "Projects section missing"
        )
        suggestions.append(
            "Add academic or personal projects"
        )

    # Internship
    if "intern" in text or "experience" in text:
        score += 10
        strengths.append(
            "Experience section present"
        )
    else:
        weaknesses.append(
            "No internship experience found"
        )
        suggestions.append(
            "Add internships or practical experience"
        )

    # Achievements
    if "%" in text or "improved" in text or "increased" in text:
        score += 10
        strengths.append(
            "Quantified achievements detected"
        )
    else:
        weaknesses.append(
            "No measurable achievements found"
        )
        suggestions.append(
            "Add metrics and quantified achievements"
        )

    score = min(score, 100)

    return {
        "resume_score": score,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions
    }