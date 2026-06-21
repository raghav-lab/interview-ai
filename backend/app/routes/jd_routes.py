from fastapi import APIRouter

router = APIRouter()


@router.post("/match-jd")
def match_jd():

    return {
        "match_score": 82,

        "matching_skills": [
            "React",
            "FastAPI",
            "PostgreSQL",
            "Python"
        ],

        "missing_skills": [
            "Docker",
            "AWS",
            "CI/CD"
        ],

        "recommendations": [
            "Learn Docker",
            "Study AWS basics",
            "Practice CI/CD pipelines"
        ]
    }