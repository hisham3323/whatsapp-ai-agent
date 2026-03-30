from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Create the async engine.
# We set pool sizes to handle concurrent incoming webhook requests effectively.
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG, # Logs SQL queries if DEBUG is True
    future=True,
    pool_size=5,
    max_overflow=10
)

# Create a sessionmaker specifically for async sessions
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# This is the base class for all our SQLAlchemy models
Base = declarative_base()

# Dependency to get the DB session in our FastAPI routes
async def get_db():
    """
    Yields an active database session and ensures it gets closed 
    when the request is finished.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()