# models/analysis.py — Defines the "analyses" table in PostgreSQL
# Stores the intelligence Claude extracts for each competitor

from datetime import datetime
from sqlalchemy import String, DateTime, Float, ForeignKey, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Foreign key — links this analysis to a specific competitor
    # "competitors.id" means: the "id" column in the "competitors" table
    competitor_id: Mapped[int] = mapped_column(ForeignKey("competitors.id"), nullable=False)

    # Pricing intelligence
    pricing_model: Mapped[str] = mapped_column(String(100), nullable=True)  # e.g. "freemium", "per-seat"
    pricing_min: Mapped[float] = mapped_column(Float, nullable=True)         # Lowest tier price
    pricing_max: Mapped[float] = mapped_column(Float, nullable=True)         # Highest tier price

    # Signals extracted by Claude (stored as flexible JSON)
    # JSON lets you store any structure: lists, dicts, nested data
    features: Mapped[dict] = mapped_column(JSON, nullable=True)       # Key product features
    strengths: Mapped[dict] = mapped_column(JSON, nullable=True)      # What they do well
    weaknesses: Mapped[dict] = mapped_column(JSON, nullable=True)     # Where they fall short
    target_market: Mapped[str] = mapped_column(String(500), nullable=True)  # Who they sell to

    # Raw scraped content — saved for debugging or re-processing
    raw_scraped_content: Mapped[str] = mapped_column(String(50000), nullable=True)

    # G2 review data
    g2_rating: Mapped[float] = mapped_column(Float, nullable=True)    # e.g. 4.5
    g2_review_count: Mapped[int] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationship back to the competitor
    competitor: Mapped["Competitor"] = relationship("Competitor", back_populates="analyses")

    def __repr__(self):
        return f"<Analysis: competitor_id={self.competitor_id}>"
