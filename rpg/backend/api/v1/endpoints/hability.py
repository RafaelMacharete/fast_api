from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from models.hability import Hability
from schemas.hability_schema import HabilityResponseSchema, HabilityCreateSchema
from core.deps import get_session

router = APIRouter()

@router.get('/', response_model=List[HabilityResponseSchema])
async def list_habilities(db: AsyncSession = Depends(get_session)):
    query = select(Hability)
    result = await db.execute(query)
    habilities = result.scalars().all()
    return habilities


@router.post("/", response_model=HabilityResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_hability(hability: HabilityCreateSchema, db: AsyncSession = Depends(get_session)):
    new_hability = Hability(**hability.model_dump())
    db.add(new_hability)
    await db.commit()
    await db.refresh(new_hability)
    return new_hability


@router.put("/{hability_id}", response_model=HabilityResponseSchema)
async def edit_hability(hability_id: int, hability_data: HabilityCreateSchema, db: AsyncSession = Depends(get_session)):
    query = select(Hability).filter(Hability.id == hability_id)
    result = await db.execute(query)
    hability = result.scalar_one_or_none()

    if not hability:
        raise HTTPException(status_code=404, detail="Hability not found.")

    for field, value in hability_data.model_dump().items():
        setattr(hability, field, value)

    await db.commit()
    await db.refresh(hability)
    return hability


@router.delete("/{hability_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hability(hability_id: int, db: AsyncSession = Depends(get_session)):
    query = select(Hability).filter(Hability.id == hability_id)
    result = await db.execute(query)
    hability = result.scalar_one_or_none()

    if not hability:
        raise HTTPException(status_code=404, detail="Hability not found.")

    await db.delete(hability)
    await db.commit()
    return None