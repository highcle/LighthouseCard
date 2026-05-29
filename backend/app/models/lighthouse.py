from datetime import datetime
from typing import Optional
from sqlalchemy import Integer, String, Float, Boolean, Text, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from ..database import Base


class Lighthouse(Base):
    __tablename__ = "lighthouses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    name_kana: Mapped[Optional[str]] = mapped_column(String(100))
    region: Mapped[str] = mapped_column(String(50), nullable=False)
    prefecture: Mapped[str] = mapped_column(String(20), nullable=False)
    latitude: Mapped[Optional[float]] = mapped_column(Float)
    longitude: Mapped[Optional[float]] = mapped_column(Float)
    description: Mapped[Optional[str]] = mapped_column(Text)
    card_image_url: Mapped[Optional[str]] = mapped_column(String(500))
    jcg_page_url: Mapped[Optional[str]] = mapped_column(String(500))
    qr_code_url: Mapped[Optional[str]] = mapped_column(String(500))
    established_year: Mapped[Optional[int]] = mapped_column(Integer)
    is_climbable: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user_cards: Mapped[list["UserCard"]] = relationship("UserCard", back_populates="lighthouse")
