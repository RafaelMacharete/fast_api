from sqlalchemy import Table, Column, Integer, ForeignKey
from core.configs import settings

character_hability = Table(
    'character_hability',
    settings.DBBaseModel.metadata,
    Column('character_id', Integer, ForeignKey('characters.id'), primary_key=True),
    Column('hability_id', Integer, ForeignKey('habilities.id'), primary_key=True)
)