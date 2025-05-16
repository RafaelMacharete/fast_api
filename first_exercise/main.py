from fastapi import FastAPI, HTTPException, status, Response, Depends
from models import Base, engine, SessionLocal, Character, List, Skill, CharacterSkill
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from schemas import *

app = FastAPI(title='CHARACTER API', version='beta', description='How to')
Base.metadata.create_all(bind=engine)

def db_connect():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/characters/', response_model=CharacterResponse)
def create_character(charac: CharacterCreate, db:Session=Depends(db_connect)):
    db_character = Character(**charac.model_dump())
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
    return db.query(Character).offset(skip).limit(limit=limit).all()
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

@app.post("/skills/", response_model=SkillResponse)
def create_skill(skill: SkillCreate, db: Session = Depends(db_connect)):
    db_skill = Skill(**skill.model_dump())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

@app.post("/characters/{character_id}/skills/{skill_id}", response_model=CharacterSkillResponse)
def add_skill_to_character(character_id: int, skill_id: int, db: Session = Depends(db_connect)):
    character = db.query(Character).filter(Character.id == character_id).first()
    skill = db.query(Skill).filter(Skill.id == skill_id).first()

    if not character or not skill:
        raise HTTPException(status_code=404, detail="Character or Skill not found")

    association = CharacterSkill(character_id=character.id, skill_id=skill.id)
    db.add(association)
    db.commit()
    db.refresh(association)
    return association

@app.post("/battle/")
def battle(char1_id: int, char2_id: int, db: Session = Depends(db_connect)):
    char1 = db.query(Character).filter(Character.id == char1_id).first()
    char2 = db.query(Character).filter(Character.id == char2_id).first()

    if not char1 or not char2:
        raise HTTPException(status_code=404, detail="Character not found")

    score1 = char1.strength + char1.agility + char1.defense
    score2 = char2.strength + char2.agility + char2.defense

    if score1 > score2:
        winner = char1.name
    elif score2 > score1:
        winner = char2.name
    else:
        winner = "Draw"

    return {"winner": winner, "char1_score": score1, "char2_score": score2}