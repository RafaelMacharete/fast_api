from sqlalchemy import create_engine, Column, Integer, String
from typing import Optional, Any, List
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

DATABASE_URL = 'sqlite:///./character.db'
# ----------------------Django Settings -----------------------------------
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
'''

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    strength = Column(Integer, index=True)
    defense = Column(Integer, index=True)
    agility = Column(Integer, index=True)
    

class Skill(Base):
    __tablename__ = 'skills'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    power = Column(Integer)
    type = Column(String)  # 'attack', 'deffense', 'support'

    characters = relationship("CharacterSkill", back_populates="skill")

class CharacterSkill(Base):
    __tablename__ = 'character_skills'

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey('characters.id'))
    skill_id = Column(Integer, ForeignKey('skills.id'))

    character = relationship("Character", back_populates="skills")
    skill = relationship("Skill", back_populates="characters")

Character.skills = relationship("CharacterSkill", back_populates="character")