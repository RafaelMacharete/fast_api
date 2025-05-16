from pydantic.v1 import BaseSettings # This set all configs to our models on database
from sqlalchemy.orm import declarative_base # All resources from our sqlachemy

class Settings(BaseSettings):
    '''General settings of API'''
    
    API_V1_STR:str = '/api/v1'
    # API_V2_STR:str = '/api/v2'
    
    DB_URL: str = 'mysql+asyncmy://root@127.0.0.1:3306/lol'
    
    DBBaseModel = declarative_base() # When we call this, It inherits.
    
class Config:
    '''Patterns config'''

    case_sensitive = False
    env_file = '.venv' # Name of ur env file

settings = Settings()