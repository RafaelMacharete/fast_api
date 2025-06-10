from core.configs import settings
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.character_hability_association import character_hability

class Hability(settings.DBBaseModel):
    __tablename__ = 'habilities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256))
    physical_damage = Column(Integer)
    magic_damage = Column(Integer)
    description = Column(String(256))

    characters = relationship(
        'Character',
        secondary=character_hability,
        back_populates='habilities'
    )
