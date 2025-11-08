from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin
import uuid


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relationships
    jobs = relationship("Job", back_populates="user", cascade="all, delete-orphan")
