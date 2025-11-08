from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import User
from app.models.icp import ICP
from app.models.job import Job
from app.schemas.icp import ICPResponse, ICPUpdate
from app.api.dependencies.auth import get_current_user

router = APIRouter()


@router.get("/{icp_id}", response_model=ICPResponse)
async def get_icp(
    icp_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get an ICP by ID"""
    result = await db.execute(
        select(ICP).join(Job).where(ICP.id == icp_id, Job.user_id == current_user.id)
    )
    icp = result.scalar_one_or_none()

    if not icp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ICP not found"
        )

    return icp


@router.patch("/{icp_id}", response_model=ICPResponse)
async def update_icp(
    icp_id: str,
    icp_update: ICPUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update an ICP"""
    result = await db.execute(
        select(ICP).join(Job).where(ICP.id == icp_id, Job.user_id == current_user.id)
    )
    icp = result.scalar_one_or_none()

    if not icp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ICP not found"
        )

    # Update fields
    update_data = icp_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(icp, field, value)

    await db.commit()
    await db.refresh(icp)

    return icp
