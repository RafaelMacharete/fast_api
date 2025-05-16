from core.configs import settings
from sqlalchemy import Column, Integer, Boolean, Float, String

class ChampionModel(settings.DBBaseModel):
    __tablename__ = 'champion'

    id:int = Column(Integer(), primary_key=True, autoincrement=True)
    name:str = Column(String(256))
    age:int = Column(Integer())
    region:str = Column(String(100))
    image:str = Column(String(256))

    hp:int = Column(Integer())
    physical_damage:int = Column(Integer())
    magic_damage:int = Column(Integer())
    defense:int = Column(Integer())
    movement_speed:int = Column(Integer())
