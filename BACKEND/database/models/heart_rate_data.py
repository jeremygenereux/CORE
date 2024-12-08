from sqlalchemy import Integer, String, ForeignKey, DateTime
from database.database import Database
from sqlalchemy.orm import (
    mapped_column,
    relationship,
    Mapped,
)
from datetime import datetime

# Model for the HeartRateData table
class HeartRateData(Database.Base):
    __tablename__ = "HeartRateData"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    device_id: Mapped[str] = mapped_column(String, ForeignKey("Device.id"))
    game_id: Mapped[int] = mapped_column(ForeignKey("Game.id"))
    heart_rate: Mapped[int] = mapped_column(Integer)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Relations
    device: Mapped["Device"] = relationship("Device", back_populates="heart_rate_data")
    game: Mapped["Game"] = relationship("Game", back_populates="heart_rate_data")

    def __repr__(self) -> str:
        return f"<HeartRateData(heart_rate={self.heart_rate}, timestamp={self.timestamp}, device_id={self.device_id})>"
