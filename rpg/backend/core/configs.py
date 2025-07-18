from pydantic.v1 import BaseSettings
from sqlalchemy.orm import declarative_base

class Settings(BaseSettings):
    '''
    Initital settings used on application
    '''
    
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'sqlite+aiosqlite:///./rpg.db'
    DBBaseModel = declarative_base() # It servers to models inherit all resources from sqlalchemy
    
class Config:
    case_sensitive = False
    env_file = '.venv'

settings = Settings()