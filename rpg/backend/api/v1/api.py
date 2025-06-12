from fastapi import APIRouter

from api.v1.endpoints import character
from api.v1.endpoints import region

api_router = APIRouter()
api_router.include_router(character.router, prefix='/character', tags=['characters'])
api_router.include_router(region.router, prefix='/region', tags=['regions'])