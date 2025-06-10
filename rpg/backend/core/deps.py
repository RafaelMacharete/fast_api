from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import Session

async def get_session() -> Generator:
    '''
    That function has a return as a generator
    '''
    session: AsyncSession = Session()
    try:
        yield session  # Return a session, but still alives
    finally:
        await session.close() # After using the session to database, we close it