from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import competitors, analysis

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created / verified")
    yield
    await engine.dispose()

app = FastAPI(
    title=settings.APP_NAME,
    description="Competitive intelligence powered by Claude AI and Firecrawl",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(competitors.router)
app.include_router(analysis.router)

@app.get("/")
async def root():
    return {
        "message": f"{settings.APP_NAME} is running",
        "docs": "/docs",
        "status": "healthy"
    }
