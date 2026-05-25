# database.py — Sets up the connection to PostgreSQL
# SQLAlchemy is the tool that lets Python talk to the database
# "async" means the app doesn't freeze while waiting for DB responses

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


# The "engine" is the actual connection to your PostgreSQL database
# It uses the DATABASE_URL from your .env file
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # When DEBUG=True, prints all SQL queries to console (helpful for learning)
)

# A "session" is like a conversation with the database
# Each request to your API gets its own session, then it closes when done
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Keeps data accessible after saving to DB
)


# Base class that all your database models will inherit from
# This is what lets SQLAlchemy know a class represents a database table
class Base(DeclarativeBase):
    pass


# This function provides a database session to your routes
# It's a "dependency" — FastAPI automatically calls it when a route needs the DB
# The "yield" makes it a generator: opens session → route runs → closes session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session          # Hand the session to the route
            await session.commit() # Save any changes made during the request
        except Exception:
            await session.rollback()  # Undo changes if something went wrong
            raise
