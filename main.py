from fastapi import FastAPI, HTTPException, status, Response, Depends
from typing import Optional, Any, List

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import Session
from pydantic import BaseModel

DATABASE_URL = 'sqlite:///./character.db'

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(title='CHARACTER API', version='beta', description='How to')

class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    strength = Column(Integer, index=True)
    defense = Column(Integer, index=True)
    agility = Column(Integer, index=True)

Base.metadata.create_all(bind=engine)

    
def db_connect():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CharacterCreate(BaseModel):
    id: int
    name: str
    strength: int
    defense: int
    agility: int

class CharacterResponse(BaseModel):
    id: int
    name: str
    strength: int
    defense: int
    agility: int
    
class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    strength: Optional[int] = None
    defense: Optional[int] = None
    agility: Optional[int] = None

@app.post('/characters/', response_model=CharacterResponse)
def create_character(charac: CharacterCreate, db:Session=Depends(db_connect)):
    db_character = Character(
        id=charac.id, 
        name=charac.name, 
        strength=charac.strength, 
        defense=charac.defense,
        agility=charac.agility
        )
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character

@app.get('/characters/', response_model=List[CharacterResponse])
def read_characters(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(db_connect)
    ):
    characters = db.query(Character).offset(skip).limit(limit).all()    
    return characters

@app.get('/characters/{character_id}', response_model=CharacterResponse)
def read_user_by_id(
    charac_id:int, 
    db: Session = Depends(db_connect)
    ):
    character_by_id = db.query(Character).filter(Character.id == charac_id).first()

    if not character_by_id:
        raise HTTPException(status_code=404, detail='Character not found') 

    return character_by_id

@app.post('/characters/{character_id}', response_model=CharacterResponse)
def update_character(charac_id:int, charac: CharacterUpdate, db: Session = Depends(db_connect)):
    db_character = db.query(Character).filter(Character.id == charac_id).first()
    if not db_character:
        raise HTTPException(status_code=404, detail='Character not found')
    db_character.name = charac.name if charac.name else db_character.name
    db_character.strength = charac.strength if charac.strength else db_character.strength
    db_character.defense = charac.defense if charac.defense else db_character.defense
    db_character.agility = charac.agility if charac.agility else db_character.agility 
    db.commit()
    db.refresh(db_character)
    return db_character

@app.delete('/characters/{character_id}', response_model=CharacterResponse)
def delete_characeter(charac_id:int, db:Session = Depends(db_connect)):
    db_character = db.query(Character).filter(Character.id == charac_id).first()

    if not db_character:
        raise HTTPException(status_code=404, detail='Character not found')

    db.delete(db_character)
    db.commit()
    return db_character

@app.patch('/characters/{character_id}', response_model=CharacterResponse)
def partial_update_character(character_id: int, charac: CharacterUpdate, db: Session = Depends(db_connect)):
    db_character = db.query(Character).filter(Character.id == character_id).first()
    if not db_character:
        raise HTTPException(status_code=404, detail='Character not found')
    
    character_data = charac.model_dump(exclude_unset=True)
    
    if "name" in character_data:
        existing_character = db.query(Character).filter(
            Character.name == character_data["name"],
            Character.id != character_id
        ).first()
        if existing_character:
            raise HTTPException(status_code=400, detail="Character name already in use")

    for key, value in character_data.items():
        setattr(db_character, key, value)

    db.commit()
    db.refresh(db_character)
    return db_character
