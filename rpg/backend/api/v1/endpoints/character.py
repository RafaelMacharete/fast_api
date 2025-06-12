from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.character import Character
from models.region import Region
from schemas.character_schema import CharacterCreateSchema, CharacterResponseSchema
from core.deps import get_session

from sqlalchemy.orm import selectinload
router = APIRouter()

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=CharacterResponseSchema)
async def create_character(character: CharacterCreateSchema, db: AsyncSession = Depends(get_session)):
    """
    Create a new character in the database.
    """
    # Verify if region exists
    query = select(Region).filter(Region.id == character.region_id)
    result = await db.execute(query)
    region = result.scalar_one_or_none()

    if not region:
        raise HTTPException(status_code=400, detail="Region ID is invalid.")

    # Create character normally
    new_character = Character(**character.model_dump())
    db.add(new_character)
    await db.commit()
    await db.refresh(new_character)
    return new_character

@router.get('/retrieve', status_code=status.HTTP_200_OK, response_model=List[CharacterResponseSchema])
async def retrieve_all_characters(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Character).options(selectinload(Character.region))
        result = await session.execute(query)
        characters: List[Character] = result.scalars().all()
        return characters

@router.get('/retrieve', status_code=status.HTTP_200_OK, response_model=List[CharacterResponseSchema])
async def retrieve_all_characters(db: AsyncSession = Depends(get_session)):
    """
    Retrieve all characters from the database.
    Returns a list of characters.
    """
    async with db as session:
        query = select(Character).options(selectinload(Character.region))
        result = await session.execute(query)
        characters: List[Character] = result.scalars().all()
        return characters

@router.get('/retrieve/{character_id}', status_code=status.HTTP_200_OK, response_model=CharacterResponseSchema)
async def retrieve_specific_character(character_id: int, db: AsyncSession = Depends(get_session)):
    """
    Retrieve a specific character by ID.
    """
    async with db as session:
        query = select(Character).options(selectinload(Character.region)).filter(Character.id == character_id)
        result = await session.execute(query)
        character = result.scalar_one_or_none()

    if character:
        return character
    raise HTTPException(detail='Character not found.', status_code=status.HTTP_404_NOT_FOUND)

@router.put('/edit/{character_id}', status_code=status.HTTP_202_ACCEPTED, response_model=CharacterResponseSchema)
async def edit_character(character_id: int, character: CharacterCreateSchema, db: AsyncSession = Depends(get_session)):
    """
    Edit an existing character by ID.
    """
    async with db as session:
        query = select(Character).filter(Character.id == character_id)
        result = await session.execute(query)
        character_update = result.scalar_one_or_none()

    if not character_update:
        raise HTTPException(detail='Character not found.', status_code=status.HTTP_404_NOT_FOUND)

    # Verify if region exists
    query = select(Region).filter(Region.id == character.region_id)
    result = await session.execute(query)
    region = result.scalar_one_or_none()

    if not region:
        raise HTTPException(status_code=400, detail="Region ID is invalid.")

    # Update fields
    data = character.model_dump()
    for field, value in data.items():
        setattr(character_update, field, value)

    await db.commit()
    await db.refresh(character_update)
    return character_update

@router.delete('/delete/{character_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_character(character_id: int, db: AsyncSession = Depends(get_session)):
    """
    Delete a character by ID.
    """
    async with db as session:
        query = select(Character).filter(Character.id == character_id)
        result = await session.execute(query)
        character_delete = result.scalar_one_or_none()

    if character_delete:
        await session.delete(character_delete)
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(detail='Character not found.', status_code=status.HTTP_404_NOT_FOUND)
