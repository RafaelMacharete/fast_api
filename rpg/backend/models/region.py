from core.configs import settings
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Region(settings.DBBaseModel):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(256), nullable=True)

    characters = relationship('Character', back_populates='region', cascade='all, delete-orphan')