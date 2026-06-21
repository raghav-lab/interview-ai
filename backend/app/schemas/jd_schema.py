from pydantic import BaseModel

class JDRequest(BaseModel):
    resume_id: int
    job_description: str