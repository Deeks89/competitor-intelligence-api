from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.competitor import Competitor
from app.schemas.competitor import CompetitorCreate, CompetitorRead
from app.services.claude_service import discover_competitors
import asyncio

router = APIRouter(prefix="/api/competitors", tags=["competitors"])

@router.post("/discover", response_model=list[CompetitorRead])
async def discover_and_save_competitors(
    payload: CompetitorCreate,
    db: Session = Depends(get_db)
):
    # Check if already in DB
    existing = db.query(Competitor).filter(
        Competitor.industry == payload.industry
    ).all()
    if existing:
        return existing

    # Ask Claude to find competitors
    competitors_data = await discover_competitors(payload.company_name, payload.industry)

    # Save each to DB
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

    db.commit()
    for comp in saved:
        db.refresh(comp)

    return saved

@router.get("/", response_model=list[CompetitorRead])
def list_competitors(db: Session = Depends(get_db)):
    return db.query(Competitor).all()

@router.get("/{competitor_id}", response_model=CompetitorRead)
def get_competitor(competitor_id: int, db: Session = Depends(get_db)):
    competitor = db.query(Competitor).filter(Competitor.id == competitor_id).first()
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")
    return competitor
