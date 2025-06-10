from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.character import Character
from models.hability import Hability 
from schemas.character_schema import CharacterCreateSchema, CharacterResponseSchema

from core.deps import get_session


router = APIRouter()

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=CharacterResponseSchema)
async def create_character(character: CharacterCreateSchema, db: AsyncSession = Depends(get_session)):
    hability_ids = character.hability_ids or []
    data = character.model_dump(exclude={"hability_ids"})
    
    # Create new character without habilities
    new_character = Character(**data)

    # Search existing habilities
    if hability_ids:
        query = select(Hability).filter(Hability.id.in_(hability_ids))
        result = await db.execute(query)
        habilities = result.scalars().all()

        if len(habilities) != len(hability_ids):
            raise HTTPException(
                status_code=400,
                detail="One or more hability IDs are invalid."
            )

        new_character.habilities = habilities

    db.add(new_character)
    await db.commit()
    await db.refresh(new_character)
    return new_character


@router.get('/retrieve', status_code=status.HTTP_200_OK, response_model=List[CharacterResponseSchema])
async def retrieve_all_characters(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Character)
        result = await session.execute(query)
        characters: List[Character] = result.scalars().all()
        return characters


@router.get('/retrieve/{character_id}', status_code=status.HTTP_200_OK, response_model=CharacterResponseSchema)
async def retrieve_specific_character(character_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Character).filter(Character.id == character_id)
        result = await session.execute(query)
        character = result.scalar_one_or_none()

        if character:
            return character
        else:
            raise HTTPException(detail='Character not found.', status_code=status.HTTP_404_NOT_FOUND)


@router.put('/edit/{character_id}', status_code=status.HTTP_202_ACCEPTED, response_model=CharacterResponseSchema)
async def edit_character(character_id: int, character: CharacterCreateSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Character).filter(Character.id == character_id)
        result = await session.execute(query)
        character_update = result.scalar_one_or_none()

        if not character_update:
            raise HTTPException(detail='Character not found.', status_code=status.HTTP_404_NOT_FOUND)

        hability_ids = character.hability_ids or []
        data = character.model_dump(exclude={"hability_ids"})

        # Update fields from character
        for field, value in data.items():
            setattr(character_update, field, value)

        # Update the habilities, if sent
        if hability_ids:
            query = select(Hability).filter(Hability.id.in_(hability_ids))
            result = await session.execute(query)
            habilities = result.scalars().all()

            if len(habilities) != len(hability_ids):
                raise HTTPException(
                    status_code=400,
                    detail="One or more hability IDs are invalid."
                )

            character_update.habilities = habilities

        await session.commit()
        await session.refresh(character_update)
        return character_update


@router.delete('/delete/{character_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_character(character_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Character).filter(Character.id == character_id)
        result = await session.execute(query)
        character_delete = result.scalar_one_or_none()

        if character_delete:
            await session.delete(character_delete)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Character not found.', status_code=status.HTTP_404_NOT_FOUND)
