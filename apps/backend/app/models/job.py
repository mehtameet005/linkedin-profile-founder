from sqlalchemy import Column, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin
import uuid
import enum


class JobStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Job(Base, TimestampMixin):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    website_url = Column(String, nullable=False)
    status = Column(
        SQLEnum(JobStatus), default=JobStatus.PENDING, nullable=False, index=True
    )

    # Relationships
    user = relationship("User", back_populates="jobs")
    icp = relationship(
        "ICP", back_populates="job", uselist=False, cascade="all, delete-orphan"
    )
    candidates = relationship("Candidate", back_populates="job", cascade="all, delete-orphan")
