from pydantic import BaseModel
from typing import Optional

class CharacterBase(BaseModel):
    name:str
    strength:int
    defense:int
    agility:int

class CharacterCreate(CharacterBase):
    pass

class CharacterResponse(CharacterBase):
    id: int
    
    class Config:
        orm_mode = True
    
class CharacterUpdate(CharacterBase):
    name: Optional[str] = None
    strength: Optional[int] = None
    defense: Optional[int] = None
    agility: Optional[int] = None

class SkillBase(BaseModel):
    name: str
    power: int
    type: str

class SkillCreate(SkillBase):
    pass

class SkillResponse(SkillBase):
    id: int

    class Config:
        orm_mode = True

class CharacterSkillResponse(BaseModel):
    character_id: int
    skill: SkillResponse

    class Config:
        orm_mode = True