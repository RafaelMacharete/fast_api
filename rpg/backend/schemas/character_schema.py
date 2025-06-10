from typing import List, Optional
from pydantic import BaseModel as SCBaseModel
from schemas.hability_schema import HabilityResponseSchema

class CharacterCreateSchema(SCBaseModel):
    name: str
    age: int
    region: str
    image: str

    hp: int
    physical_damage: int
    magic_damage: int
    armor_defense: int
    magic_defense: int
    movement_speed: int

    hability_ids: Optional[List[int]]  # List of IDs on POST

class CharacterResponseSchema(CharacterCreateSchema):
    id: int
    habilities: List[HabilityResponseSchema]  # Return the objects, and not IDs

    class Config:
        orm_mode = True