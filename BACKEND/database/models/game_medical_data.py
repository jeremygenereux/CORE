from sqlalchemy import Integer, ForeignKey, DateTime
from database.database import Database
from sqlalchemy.orm import (
    mapped_column,
    relationship,
    Mapped,
)
from datetime import datetime
from database.models.player import Player

# Model for the GameMedicalData table
class GameMedicalData(Database.Base):
    __tablename__ = "GameMedicalData"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("Player.id"))
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    max_HR: Mapped[int] = mapped_column(Integer, nullable=False)
    rest_HR: Mapped[int] = mapped_column(Integer, nullable=False)
    zone1_min_HR: Mapped[int] = mapped_column(Integer, nullable=False)
    zone2_min_HR: Mapped[int] = mapped_column(Integer, nullable=False)
    zone3_min_HR: Mapped[int] = mapped_column(Integer, nullable=False)
    zone4_min_HR: Mapped[int] = mapped_column(Integer, nullable=False)
    zone5_min_HR: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relations
    player: Mapped["Player"] = relationship("Player", back_populates="medical_data")

    def __repr__(self) -> str:
        return f"<GameMedicalData(player_id={self.player_id}, timestamp={self.timestamp}, max_HR={self.max_HR}, rest_HR={self.rest_HR})>"

    def __init__(self, player: Player, timestamp: datetime, max_HR: int, rest_HR: int):
        super().__init__()
        self.player = player
        self.timestamp = timestamp
        self.rest_HR = rest_HR
        self.calculate_zones(rest_HR, max_HR)

    def calculate_zones(self, rest_HR, max_HR):
        # See documentation for explanation of this formula
        fc_reserve = max_HR - rest_HR
        self.zone1_min_HR = int(rest_HR + fc_reserve * 0.5)
        self.zone2_min_HR = int(rest_HR + fc_reserve * 0.6)
        self.zone3_min_HR = int(rest_HR + fc_reserve * 0.7)
        self.zone4_min_HR = int(rest_HR + fc_reserve * 0.8)
        self.zone5_min_HR = int(rest_HR + fc_reserve * 0.9)
        self.max_HR = max_HR

    @staticmethod
    def calculate_max_HR(age):
        # See documentation for explanation of this formula
        return round(202.5 - (0.53 * age))