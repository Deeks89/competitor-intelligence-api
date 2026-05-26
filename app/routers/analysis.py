from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.competitor import Competitor
from app.models.analysis import Analysis
from app.schemas.analysis import AnalysisRead
from app.services.claude_service import extract_signals
from app.services.firecrawl_service import scrape_competitor_website, scrape_g2_page

router = APIRouter(prefix="/api/analysis", tags=["analysis"])

@router.post("/{competitor_id}/run", response_model=AnalysisRead)
async def analyze_competitor(competitor_id: int, db: AsyncSession = Depends(get_db)):
    # Step 1 — find the competitor in DB
    result = await db.execute(select(Competitor).where(Competitor.id == competitor_id))
    competitor = result.scalar_one_or_none()
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")

    # Step 2 — check if analysis already exists (dedup)
    existing = await db.execute(select(Analysis).where(Analysis.competitor_id == competitor_id))
    existing_analysis = existing.scalar_one_or_none()
    if existing_analysis:
        return existing_analysis

    # Step 3 — scrape competitor website via Firecrawl
    website_content = ""
    if competitor.website:
        website_content = await scrape_competitor_website(competitor.website)

    # Step 4 — scrape G2 page for reviews and ratings
    g2_content = await scrape_g2_page(competitor.name)

    # Step 5 — combine both sources and send to Claude
    combined_content = f"WEBSITE CONTENT:\n{website_content}\n\nG2 REVIEWS:\n{g2_content}"
    signals = await extract_signals(combined_content, competitor.name)

    # Step 6 — save to analyses table
    analysis = Analysis(
        competitor_id=competitor_id,
        pricing_model=signals.get("pricing_model"),
        pricing_min=signals.get("pricing_min"),
        pricing_max=signals.get("pricing_max"),
        features=signals.get("features"),
        strengths=signals.get("strengths"),
        weaknesses=signals.get("weaknesses"),
        target_market=signals.get("target_market"),
        raw_scraped_content=combined_content[:10000],
    )
    db.add(analysis)
    await db.flush()
    return analysis

@router.get("/{competitor_id}", response_model=AnalysisRead)
async def get_analysis(competitor_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Analysis).where(Analysis.competitor_id == competitor_id))
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis
