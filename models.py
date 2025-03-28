from pydantic import BaseModel




class UserCreate(BaseModel):
    name: str
    strength: int
    defense: int
    agility: int