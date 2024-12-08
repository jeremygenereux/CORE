from database.database import Database
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import (
    mapped_column,
    relationship,
    Mapped,
)
from datetime import datetime


# Model for the PlayerDeviceAt table
class PlayerDeviceAt(Database.Base):
    __tablename__ = "PlayerDeviceAt"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    device_id: Mapped[str] = mapped_column(String, ForeignKey("Device.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("Player.id"))
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Relations
    device: Mapped["Device"] = relationship("Device", back_populates="player_device_at")
    player: Mapped["Player"] = relationship("Player", back_populates="player_device_at")

    def __repr__(self) -> str:
        return f"<CurrentPlayerDevice(device_id={self.device_id}, player_id={self.player_id})>"