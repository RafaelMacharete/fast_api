from core.configs import settings
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Character(settings.DBBaseModel):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256))
    age = Column(Integer)
    image = Column(String(256))

    hp = Column(Integer)
    physical_damage = Column(Integer)
    magic_damage = Column(Integer)
    armor_defense = Column(Integer)
    magic_defense = Column(Integer)
    movement_speed = Column(Integer)

    region_id = Column(Integer, ForeignKey('regions.id'), nullable=False)
    region = relationship('Region', back_populates='characters')
