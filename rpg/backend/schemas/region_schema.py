from pydantic import BaseModel

class RegionCreateSchema(BaseModel):
    name: str
    description: str

class RegionResponseSchema(RegionCreateSchema):
    id: int

    class Config:
        orm_mode = True
