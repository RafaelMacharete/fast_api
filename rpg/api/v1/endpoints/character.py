from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.character import Character
from schemas.character_schema import CharacterSchema
from core.deps import get_session

router = APIRouter()

@router.post('/create-character/', status_code=status.HTTP_201_CREATED, response_model=CharacterSchema)
async def create_character(character:CharacterSchema, db: AsyncSession = Depends(get_session)):
    new_character = Character(**character.model_dump())
    
    db.add(new_character)
    await db.commit()

    return new_character