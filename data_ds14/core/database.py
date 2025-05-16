from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from core.configs import settings

engine:AsyncEngine = create_async_engine(settings.DB_URL) # We don't need to create, that function already does It.

Session:AsyncEngine = sessionmaker(
    autocommit=False,
    autoflush=False, # Discard (data that aren't used we discard It.)
    expire_on_commit=False, # After a commit, the session is gone, but with False, doesn't more.
    class_=AsyncSession,
    bind=engine
)