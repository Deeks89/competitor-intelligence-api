from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import competitors, analysis

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="Competitive intelligence powered by Claude AI and Firecrawl",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
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
        "docs": "http://localhost:8000/docs",
        "status": "healthy"
    }
