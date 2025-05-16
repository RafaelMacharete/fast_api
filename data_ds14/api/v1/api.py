from fastapi import APIRouter

from api.v1.endpoints import champion

api_router = APIRouter()

api_router.include_router(champion.router, prefix='/champion', tags=['Champion'])

# api_router.include_router(minion.router, prefix='/minion', tags=['Minion'])