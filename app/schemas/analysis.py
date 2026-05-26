from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class AnalysisRead(BaseModel):
    id: int
    competitor_id: int
    pricing_model: Optional[str] = None
    pricing_min: Optional[float] = None
    pricing_max: Optional[float] = None
    features: Optional[List[str]] = None
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None
    target_market: Optional[str] = None
    g2_rating: Optional[float] = None
    g2_review_count: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True
