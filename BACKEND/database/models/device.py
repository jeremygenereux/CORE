from database.database import Database
from sqlalchemy import String
from sqlalchemy.orm import (
    mapped_column,
    relationship,
    Mapped,
)
import typing

# Model for the Device table
class Device(Database.Base):
    __tablename__ = "Device"
    id: Mapped[str] = mapped_column(primary_key=True)  # No autoincrement, string ID
    brand: Mapped[typing.Optional[str]] = mapped_column(String)
    model: Mapped[typing.Optional[str]] = mapped_column(String)

    # Relations
    heart_rate_data: Mapped[typing.List["HeartRateData"]] = relationship("HeartRateData", back_populates="device")
    player_device_at: Mapped[typing.List["PlayerDeviceAt"]] = relationship("PlayerDeviceAt", back_populates="device")

    def __repr__(self) -> str:
        return f"<Device(id={self.id}, brand={self.brand}, model={self.model})>"
