from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PersonaCreate(BaseModel):
    icp_id: str
    persona_name: str
    titles: list[str]
    goals: list[str]
    pains: list[str]
    kpis: list[str]
    keywords: list[str]


class PersonaUpdate(BaseModel):
    persona_name: Optional[str] = None
    titles: Optional[list[str]] = None
    goals: Optional[list[str]] = None
    pains: Optional[list[str]] = None
    kpis: Optional[list[str]] = None
    keywords: Optional[list[str]] = None


class PersonaResponse(BaseModel):
    id: str
    icp_id: str
    persona_name: str
    titles: list[str]
    goals: list[str]
    pains: list[str]
    kpis: list[str]
    keywords: list[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
