from sqlalchemy import Column, Integer, Text, ForeignKey

from app.database.connection import Base


class InterviewQuestion(Base):

    __tablename__ = "interview_questions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    interview_id = Column(Integer)

    question = Column(Text)

    answer = Column(Text)

    score = Column(Integer)

    feedback = Column(Text)