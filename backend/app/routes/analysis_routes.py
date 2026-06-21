from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/interview/{interview_id}/weakness-analysis"
)
def weakness_analysis(interview_id: int):

    return {
        "weak_topics": [
            "Time Complexity",
            "JavaScript Event Loop"
        ],

        "strong_topics": [
            "React",
            "FastAPI",
            "Python"
        ],

        "recommended_topics": [
            "Binary Search",
            "SQL Indexing",
            "System Design"
        ],

        "learning_plan": [
            "Solve 5 DSA problems daily",
            "Study DBMS indexing",
            "Build one REST API project"
        ]
    }