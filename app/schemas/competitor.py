# models/competitor.py — Defines the "competitors" table in PostgreSQL
# Each class = one table. Each class variable = one column.

from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Competitor(Base):
    # The actual table name in PostgreSQL
    __tablename__ = "competitors"

    # Columns:
    id: Mapped[int] = mapped_column(primary_key=True)               # Auto-incrementing ID
    name: Mapped[str] = mapped_column(String(255), nullable=False)  # Company name
    website: Mapped[str] = mapped_column(String(500), nullable=True) # e.g. "https://stripe.com"
    industry: Mapped[str] = mapped_column(String(255), nullable=True) # e.g. "Payments"
    description: Mapped[str] = mapped_column(String(2000), nullable=True) # Short summary

    # Timestamps — automatically set by the database
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationship: one competitor can have many analyses
    # This lets you do competitor.analyses to get all analyses for that competitor
    analyses: Mapped[list["Analysis"]] = relationship("Analysis", back_populates="competitor")

    def __repr__(self):
        # How this object prints when you debug — e.g. <Competitor: Stripe>
        return f"<Competitor: {self.name}>"
