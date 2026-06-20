from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database.connection import Base


class Resume(Base):

    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String(255))

    resume_text = Column(Text)

    extracted_skills = Column(Text)

    user_id = Column(Integer)