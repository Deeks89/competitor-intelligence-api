# main.py — The entry point of your entire API
# FastAPI starts here, registers all routes, and handles startup/shutdown

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.routers import competitors, analysis


# "lifespan" runs code at startup and shutdown
# Here we use it to create database tables automatically when the app starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP: Create all tables defined in models/ if they don't exist yet
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created / verified")

    yield  # App runs here

    # SHUTDOWN: Close the DB connection pool cleanly
    await engine.dispose()
    print("👋 Database connections closed")


# Create the FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Competitive intelligence powered by Claude AI and Firecrawl",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allows your React frontend (on a different port/domain) to call this API
# Without this, browsers block cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],   # Allow GET, POST, PUT, DELETE etc.
    allow_headers=["*"],
)

# Register routers — this "mounts" all the routes from each router file
app.include_router(competitors.router)
app.include_router(analysis.router)


# Health check endpoint — a simple way to verify the API is running
# Visit http://localhost:8000/ in your browser to confirm
@app.get("/")
async def root():
    return {
        "message": f"{settings.APP_NAME} is running",
        "docs": "http://localhost:8000/docs",   # FastAPI auto-generates interactive docs here
        "status": "healthy"
    }
