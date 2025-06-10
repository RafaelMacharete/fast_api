from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from core.configs import settings

# sessionmaker returns a class to us
# It will open and close the connection to our database!

engine: AsyncEngine = create_async_engine(settings.DB_URL)
Session: AsyncEngine = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_ =  AsyncSession,
    bind=engine
)