from sqlalchemy import Column, String, ForeignKey, JSON, Index
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin
import uuid


class Candidate(Base, TimestampMixin):
    __tablename__ = "candidates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    linkedin_url = Column(String, nullable=False, unique=True, index=True)
    inferred_name = Column(String, nullable=True)
    inferred_title = Column(String, nullable=True)
    inferred_location = Column(String, nullable=True)
    inferred_company = Column(String, nullable=True)
    result_snippet = Column(String, nullable=False)
    scores = Column(JSON, nullable=False)
    explainability = Column(JSON, nullable=False)

    # Relationships
    job = relationship("Job", back_populates="candidates")
    feedbacks = relationship("Feedback", back_populates="candidate", cascade="all, delete-orphan")

    # Indexes for common queries
    __table_args__ = (
        Index("ix_candidates_job_id_score", "job_id"),
    )
