from fastapi import APIRouter

from api.v1.endpoints import character, hability

api_router = APIRouter()
api_router.include_router(character.router, prefix='/character', tags=['characters'])
api_router.include_router(hability.router, prefix='/hability', tags=['habilities'])