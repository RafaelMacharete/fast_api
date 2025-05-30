from core.configs import settings
from sqlalchemy import Column, Integer, String, ForeignKey

class Hability(settings.DBBaseModel):
    __tablename__ = 'habilities'

    id:int = Column(Integer, primary_key=True, autoincrement=True)
    name:str = Column(String(256))
    physical_damage:int = Column(Integer)
    magic_damage:int = Column(Integer)
    description:str = Column(String(256))