import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column, Mapped
from ..database import Base


class UserCard(Base):
    __tablename__ = "user_cards"
    __table_args__ = (UniqueConstraint("user_id", "lighthouse_id", name="uq_user_lighthouse"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    lighthouse_id: Mapped[int] = mapped_column(Integer, ForeignKey("lighthouses.id"), nullable=False)
    collected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    note: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="user_cards")
    lighthouse: Mapped["Lighthouse"] = relationship("Lighthouse", back_populates="user_cards")
