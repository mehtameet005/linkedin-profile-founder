from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional


class JobCreate(BaseModel):
    website_url: HttpUrl


class JobResponse(BaseModel):
    id: str
    user_id: str
    website_url: str
    status: str
    created_at: datetime
    updated_at: datetime
    icp_id: Optional[str] = None

    class Config:
        from_attributes = True


class JobList(BaseModel):
    jobs: list[JobResponse]
    total: int
