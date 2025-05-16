from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.minion_model import MinionModel
from schemas.minion_schema import MinionSchema
from core.deps import get_session

router = APIRouter()
