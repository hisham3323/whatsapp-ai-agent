from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Create the database engine using your .env URL
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# Create a session maker to talk to the database
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# This is the base class for our database tables
Base = declarative_base()