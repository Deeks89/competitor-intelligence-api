from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CompetitorCreate(BaseModel):
    company_name: str
    industry: str

class CompetitorRead(BaseModel):
    id: int
    name: str
    website: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
