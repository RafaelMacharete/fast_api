from typing import Optional
from pydantic import BaseModel as SCBaseModel


class CharacterSchema(SCBaseModel):
    
    id:Optional[int] = None
    name:str
    age:int
    region:str
    image:str

    hp:int
    physical_damage:int
    magic_damage:int
    armor_defense:int
    magic_defense:int
    movement_speed:int

    class Config:
        orm_mode = True