from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.db.session import get_db
from app.models.user import User
from app.models.candidate import Candidate
from app.models.job import Job
from app.schemas.candidate import CandidateResponse, CandidateList
from app.api.dependencies.auth import get_current_user

router = APIRouter()


@router.get("/job/{job_id}", response_model=CandidateList)
async def list_candidates(
    job_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    min_score: float = Query(None, ge=0, le=1),
    location: str = Query(None),
    company: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List candidates for a job with filters"""
    # Verify user owns the job
    result = await db.execute(
        select(Job).where(Job.id == job_id, Job.user_id == current_user.id)
    )
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
        )

    # Build query with filters
    query = select(Candidate).where(Candidate.job_id == job_id)

    # Apply filters (simplified for now - actual implementation would use JSON operators)
    if min_score is not None:
        # This is a placeholder - actual implementation needs JSON path query
        pass
    if location:
        query = query.where(Candidate.inferred_location.ilike(f"%{location}%"))
    if company:
        query = query.where(Candidate.inferred_company.ilike(f"%{company}%"))

    # Get total count
    total_result = await db.execute(query)
    all_candidates = total_result.scalars().all()
    total = len(all_candidates)

    # Paginate
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    candidates = result.scalars().all()

    return {
        "candidates": candidates,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(
    candidate_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific candidate"""
    result = await db.execute(
        select(Candidate)
        .join(Job)
        .where(Candidate.id == candidate_id, Job.user_id == current_user.id)
    )
    candidate = result.scalar_one_or_none()

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found"
        )

    return candidate
