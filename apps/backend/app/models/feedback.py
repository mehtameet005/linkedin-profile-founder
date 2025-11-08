from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin
import uuid


class Feedback(Base, TimestampMixin):
    __tablename__ = "feedbacks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    candidate_id = Column(
        String, ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    is_relevant = Column(Boolean, nullable=False)

    # Relationships
    candidate = relationship("Candidate", back_populates="feedbacks")
