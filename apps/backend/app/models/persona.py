from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin
import uuid


class Persona(Base, TimestampMixin):
    __tablename__ = "personas"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    icp_id = Column(String, ForeignKey("icps.id", ondelete="CASCADE"), nullable=False)
    persona_name = Column(String, nullable=False)
    titles = Column(JSON, default=list)
    goals = Column(JSON, default=list)
    pains = Column(JSON, default=list)
    kpis = Column(JSON, default=list)
    keywords = Column(JSON, default=list)

    # Relationships
    icp = relationship("ICP", back_populates="personas")
