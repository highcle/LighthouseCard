from pydantic import BaseModel
from typing import Optional


class LighthouseResponse(BaseModel):
    id: int
    name: str
    name_kana: Optional[str]
    region: str
    prefecture: str
    latitude: Optional[float]
    longitude: Optional[float]
    description: Optional[str]
    card_image_url: Optional[str]
    jcg_page_url: Optional[str]
    qr_code_url: Optional[str]
    established_year: Optional[int]
    is_climbable: bool
    is_collected: Optional[bool] = None

    model_config = {"from_attributes": True}


class LighthouseListResponse(BaseModel):
    items: list[LighthouseResponse]
    total: int


class IdentifyByUrlRequest(BaseModel):
    url: str


class RegisterFromQrRequest(BaseModel):
    name: str
    qr_code_url: str
