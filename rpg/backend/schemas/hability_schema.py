from pydantic import BaseModel

class HabilityCreateSchema(BaseModel):
    name: str
    physical_damage: int
    magic_damage: int
    description: str

class HabilityResponseSchema(HabilityCreateSchema):
    id: int

    class Config:
        orm_mode = True