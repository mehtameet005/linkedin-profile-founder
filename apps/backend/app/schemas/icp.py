from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ICPResponse(BaseModel):
    id: str
    job_id: str
    company_name: str
    industry: str
    sub_industries: list[str]
    firmographics: dict
    value_props: list[str]
    pain_points: list[str]
    trigger_events: list[str]
    tech_stack: dict
    embedding_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ICPUpdate(BaseModel):
    company_name: Optional[str] = None
    industry: Optional[str] = None
    sub_industries: Optional[list[str]] = None
    firmographics: Optional[dict] = None
    value_props: Optional[list[str]] = None
    pain_points: Optional[list[str]] = None
    trigger_events: Optional[list[str]] = None
    tech_stack: Optional[dict] = None
