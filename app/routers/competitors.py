# routers/competitors.py — URL endpoints for competitor operations
# A "router" groups related endpoints together
# These are the URLs users/frontend will call

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.competitor import Competitor
from app.schemas.competitor import CompetitorCreate, CompetitorRead
from app.services.claude_service import discover_competitors

# APIRouter is like a mini FastAPI app — groups related routes
# prefix means all routes here start with /api/competitors
router = APIRouter(prefix="/api/competitors", tags=["competitors"])


@router.post("/discover", response_model=list[CompetitorRead])
async def discover_and_save_competitors(
    payload: CompetitorCreate,        # The JSON body the user sends
    db: AsyncSession = Depends(get_db) # FastAPI auto-injects the DB session
):
    """
    Main entry point: user sends a company + industry,
    Claude discovers competitors, we save them to the DB and return them.
    """

    # Step 1: Ask Claude to find competitors
    competitors_data = await discover_competitors(payload.company_name, payload.industry)

    # Step 2: Save each competitor to the database
    saved = []
    for comp in competitors_data:
        db_competitor = Competitor(
            name=comp["name"],
            website=comp.get("website"),
            industry=payload.industry,
            description=comp.get("description"),
        )
        db.add(db_competitor)  # Stage the record (not saved yet)
        saved.append(db_competitor)

    await db.flush()  # Write to DB within this transaction (gets IDs assigned)

    return saved  # FastAPI serializes this to JSON using CompetitorRead schema


@router.get("/", response_model=list[CompetitorRead])
async def list_competitors(db: AsyncSession = Depends(get_db)):
    """
    Returns all competitors stored in the database.
    The frontend will call this to display the list.
    """
    result = await db.execute(select(Competitor))
    return result.scalars().all()


@router.get("/{competitor_id}", response_model=CompetitorRead)
async def get_competitor(competitor_id: int, db: AsyncSession = Depends(get_db)):
    """
    Returns a single competitor by their ID.
    e.g. GET /api/competitors/3 returns the competitor with id=3
    """
    result = await db.execute(select(Competitor).where(Competitor.id == competitor_id))
    competitor = result.scalar_one_or_none()

    if not competitor:
        # 404 is the standard HTTP code for "not found"
        raise HTTPException(status_code=404, detail="Competitor not found")

    return competitor
