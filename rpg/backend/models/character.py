from core.configs import settings
from models.hability import Hability
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey
from core.configs import settings


from sqlalchemy.orm import relationship
from models.hability import Hability
from models.character_hability_association import character_hability

class Character(settings.DBBaseModel):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256))
    age = Column(Integer)
    region = Column(String(100))
    image = Column(String(256))

    hp = Column(Integer)
    physical_damage = Column(Integer)
    magic_damage = Column(Integer)
    armor_defense = Column(Integer)
    magic_defense = Column(Integer)
    movement_speed = Column(Integer)

    habilities = relationship(
        'Hability',
        secondary=character_hability,
        back_populates='characters'
    )