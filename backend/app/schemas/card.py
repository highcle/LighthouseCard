from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .lighthouse import LighthouseResponse


class CardCreate(BaseModel):
    lighthouse_id: int
    note: Optional[str] = None


class CardUpdate(BaseModel):
    note: Optional[str] = None


class CardResponse(BaseModel):
    id: str
    user_id: str
    lighthouse_id: int
    collected_at: datetime
    note: Optional[str]
    lighthouse: Optional[LighthouseResponse] = None

    model_config = {"from_attributes": True}


class RegionStat(BaseModel):
    region: str
    total: int
    collected: int
    rate: float


class StatsResponse(BaseModel):
    total_lighthouses: int
    collected_count: int
    achievement_rate: float
    region_stats: list[RegionStat]
