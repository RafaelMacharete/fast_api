from fastapi import FastAPI, HTTPException, status, Response, Depends
from typing import Optional, Any
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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


@app.post('/characters/', response_model=Character)
def create_character(user: UserCreate, db:Session=Depends(db_connect)):

















