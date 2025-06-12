from pydantic import BaseModel
from typing import Optional
from schemas.region_schema import RegionResponseSchema

class CharacterCreateSchema(BaseModel):
    name: str
    age: int
    region_id: int
    image: str
    hp: int
    physical_damage: int
    magic_damage: int
    armor_defense: int
    magic_defense: int
    movement_speed: int

class CharacterResponseSchema(CharacterCreateSchema):
    id: int
    region: Optional[RegionResponseSchema]

    class Config:
        orm_mode = True