from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.api.dependencies.auth import get_current_user

router = APIRouter()


@router.post("/csv/{job_id}")
async def export_to_csv(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Export candidates to CSV"""
    # TODO: Implement CSV export
    return {"message": "CSV export functionality coming soon"}


@router.post("/hubspot/{job_id}")
async def export_to_hubspot(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Export candidates to HubSpot"""
    # TODO: Implement HubSpot integration
    return {"message": "HubSpot export functionality coming soon"}
