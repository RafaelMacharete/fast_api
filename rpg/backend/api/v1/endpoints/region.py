from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from models.region import Region
from schemas.region_schema import RegionResponseSchema, RegionCreateSchema
from core.deps import get_session

router = APIRouter()

@router.get('/', response_model=List[RegionResponseSchema])
async def list_regions(db: AsyncSession = Depends(get_session)):
    query = select(Region)
    result = await db.execute(query)
    regions = result.scalars().all()
    return regions

@router.post("/", response_model=RegionResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_region(region: RegionCreateSchema, db: AsyncSession = Depends(get_session)):
    new_region = Region(**region.model_dump())
    db.add(new_region)
    await db.commit()
    await db.refresh(new_region)
    return new_region

@router.put("/{region_id}", response_model=RegionResponseSchema)
async def edit_region(region_id: int, region_data: RegionCreateSchema, db: AsyncSession = Depends(get_session)):
    query = select(Region).filter(Region.id == region_id)
    result = await db.execute(query)
    region = result.scalar_one_or_none()

    if not region:
        raise HTTPException(status_code=404, detail="Region not found.")

    for field, value in region_data.model_dump().items():
        setattr(region, field, value)

    await db.commit()
    await db.refresh(region)
    return region

@router.delete("/{region_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_region(region_id: int, db: AsyncSession = Depends(get_session)):
    query = select(Region).filter(Region.id == region_id)
    result = await db.execute(query)
    region = result.scalar_one_or_none()

    if not region:
        raise HTTPException(status_code=404, detail="Region not found.")

    await db.delete(region)
    await db.commit()
    return None
