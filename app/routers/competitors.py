from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.competitor import Competitor
from app.schemas.competitor import CompetitorCreate, CompetitorRead
from app.services.claude_service import discover_competitors

router = APIRouter(prefix="/api/competitors", tags=["competitors"])

@router.post("/discover", response_model=list[CompetitorRead])
async def discover_and_save_competitors(
    payload: CompetitorCreate,
    db: AsyncSession = Depends(get_db)
):
    competitors_data = await discover_competitors(payload.company_name, payload.industry)
    saved = []
    for comp in competitors_data:
        db_competitor = Competitor(
            name=comp["name"],
            website=comp.get("website"),
            industry=payload.industry,
            description=comp.get("description"),
        )
        db.add(db_competitor)
        saved.append(db_competitor)
    await db.flush()
    return saved

@router.get("/", response_model=list[CompetitorRead])
async def list_competitors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Competitor))
    return result.scalars().all()

@router.get("/{competitor_id}", response_model=CompetitorRead)
async def get_competitor(competitor_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Competitor).where(Competitor.id == competitor_id))
    competitor = result.scalar_one_or_none()
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")
    return competitor
