from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional


class CandidateScores(BaseModel):
    semantic: float
    role: float
    industry: float
    geo: float
    final: float


class CandidateExplainability(BaseModel):
    keywords_matched: list[str]
    feature_contributions: dict[str, float]


class CandidateResponse(BaseModel):
    id: str
    job_id: str
    linkedin_url: str
    inferred_name: Optional[str] = None
    inferred_title: Optional[str] = None
    inferred_location: Optional[str] = None
    inferred_company: Optional[str] = None
    result_snippet: str
    scores: CandidateScores
    explainability: CandidateExplainability
    created_at: datetime

    class Config:
        from_attributes = True


class CandidateFilters(BaseModel):
    min_score: Optional[float] = None
    max_score: Optional[float] = None
    location: Optional[str] = None
    company: Optional[str] = None
    title_pattern: Optional[str] = None


class CandidateList(BaseModel):
    candidates: list[CandidateResponse]
    total: int
    page: int
    page_size: int
