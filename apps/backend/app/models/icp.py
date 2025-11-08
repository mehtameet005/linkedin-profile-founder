from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin
import uuid


class ICP(Base, TimestampMixin):
    __tablename__ = "icps"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    company_name = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    sub_industries = Column(JSON, default=list)
    firmographics = Column(JSON, default=dict)
    value_props = Column(JSON, default=list)
    pain_points = Column(JSON, default=list)
    trigger_events = Column(JSON, default=list)
    tech_stack = Column(JSON, default=dict)
    embedding_id = Column(String, nullable=True)

    # Relationships
    job = relationship("Job", back_populates="icp")
    personas = relationship("Persona", back_populates="icp", cascade="all, delete-orphan")
