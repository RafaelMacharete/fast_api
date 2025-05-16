from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.champion_model import ChampionModel
from schemas.champion_schema import ChampionSchema
from core.deps import get_session

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ChampionSchema)
async def create_champion(champion : ChampionSchema, db: AsyncSession = Depends(get_session)):
    '''
        Create a champion based on the champion schema
    '''
    new_champion = ChampionModel(name=champion.name, age=champion.age,
                                 region=champion.region, image=champion.image,
                                 hp=champion.hp, physical_damage=champion.physical_damage,
                                 magic_damage=champion.magic_damage, defense=champion.defense,
                                 movement_speed=champion.movement_speed)

    db.add(new_champion)
    await db.commit()
    return new_champion

@router.get('/', response_model=List[ChampionSchema])
async def retrieve_champions(db : AsyncSession = Depends(get_session)):
    '''
        Retrieve all champions created at moment
    '''
    async with db as session:
        query = select(ChampionModel)
        result = await session.execute(query)

        champions: List[ChampionModel] = result.scalars().all() #scalars() seems like a 'filter'

        return champions

@router.get('/{champion_id}', response_model=ChampionSchema)
async def retrieve_specific_champion(champion_id : int, db : AsyncSession = Depends(get_session)):
    '''
        By the given id on URL, retrive the champion that references that ID
    '''
    async with db as session:
        query = select(ChampionModel).filter(ChampionModel.id == champion_id)

        result = await session.execute(query)

        champion = result.scalar_one_or_none()

        if champion:
            return champion
        else:
            raise HTTPException(detail='Champion not found', 
                                status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{champion_id}', response_model=ChampionSchema, status_code=status.HTTP_201_CREATED)
async def edit_champion(champion_id : int, champion: ChampionSchema, db:AsyncSession = Depends(get_session)):
    '''
        By the given champion id at URL, update a specific champion
    '''
    async with db as session:
        query = select(ChampionModel).filter(ChampionModel.id == champion_id)

        result = await session.execute(query)

        champion_update = result.scalar_one_or_none()

        if champion_update:
            champion_update.name = champion.name 
            champion_update.age = champion.age
            champion_update.region = champion.region
            champion_update.image = champion.image
            
            champion_update.hp = champion.hp
            champion_update.physical_damage = champion.physical_damage
            champion_update.magic_damage = champion.magic_damage
            champion_update.defense = champion.defense
            champion_update.movement_speed = champion.movement_speed
            
            await db.commit()
            return champion_update
        raise HTTPException(detail='Champion not found', status_code=status.HTTP_404_NOT_FOUND)
            
@router.delete('/{champion_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_champion(champion_id : int, db : AsyncSession = Depends(get_session)):
    '''
        By the given champion id at URL, delete a specific champion
    '''
    async with db as session:
        query = select(ChampionModel).filter(ChampionModel.id == champion_id)

        result = await session.execute(query)

        champion_delete = result.scalar_one_or_none()

        if champion_delete:
            await session.delete(champion_delete)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Champion not found',
                                status_code=status.HTTP_404_NOT_FOUND)
            