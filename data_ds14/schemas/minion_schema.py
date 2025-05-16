from typing import Optional
from pydantic import BaseModel as SCBaseModel

class MinionSchema(SCBaseModel):
    
    id:Optional[int] = None
    name:str
    hp:int
    defense:int
    movement_speed:int