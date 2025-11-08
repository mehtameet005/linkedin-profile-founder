from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import User
from app.models.persona import Persona
from app.models.icp import ICP
from app.models.job import Job
from app.schemas.persona import PersonaCreate, PersonaUpdate, PersonaResponse
from app.api.dependencies.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=PersonaResponse, status_code=status.HTTP_201_CREATED)
async def create_persona(
    persona_data: PersonaCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new persona"""
    # Verify user owns the ICP
    result = await db.execute(
        select(ICP)
        .join(Job)
        .where(ICP.id == persona_data.icp_id, Job.user_id == current_user.id)
    )
    icp = result.scalar_one_or_none()

    if not icp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ICP not found"
        )

    persona = Persona(**persona_data.model_dump())
    db.add(persona)
    await db.commit()
    await db.refresh(persona)

    return persona


@router.get("/{persona_id}", response_model=PersonaResponse)
async def get_persona(
    persona_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a persona by ID"""
    result = await db.execute(
        select(Persona)
        .join(ICP)
        .join(Job)
        .where(Persona.id == persona_id, Job.user_id == current_user.id)
    )
    persona = result.scalar_one_or_none()

    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persona not found"
        )

    return persona


@router.patch("/{persona_id}", response_model=PersonaResponse)
async def update_persona(
    persona_id: str,
    persona_update: PersonaUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a persona"""
    result = await db.execute(
        select(Persona)
        .join(ICP)
        .join(Job)
        .where(Persona.id == persona_id, Job.user_id == current_user.id)
    )
    persona = result.scalar_one_or_none()

    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persona not found"
        )

    update_data = persona_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(persona, field, value)

    await db.commit()
    await db.refresh(persona)

    return persona


@router.delete("/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_persona(
    persona_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a persona"""
    result = await db.execute(
        select(Persona)
        .join(ICP)
        .join(Job)
        .where(Persona.id == persona_id, Job.user_id == current_user.id)
    )
    persona = result.scalar_one_or_none()

    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persona not found"
        )

    await db.delete(persona)
    await db.commit()
