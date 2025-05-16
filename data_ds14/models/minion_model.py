from core.configs import settings
from sqlalchemy import Column, Integer, Boolean, Float, String

class MinionModel(settings.DBBaseModel):
    __tablename__ = 'minion'

    id:int = Column(Integer(), primary_key=True, autoincrement=True)
    name:str = Column(String(100))
    hp:int = Column(Integer())
    defense:int = Column(Integer())
    movement_speed:int = Column(Integer())