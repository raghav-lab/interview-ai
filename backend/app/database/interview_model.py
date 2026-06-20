from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database.connection import Base


class Interview(Base):

    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    resume_id = Column(Integer)

    overall_score = Column(Integer, default=0)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )