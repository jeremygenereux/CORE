from sqlalchemy import Integer, String, ForeignKey, DateTime
from database.database import Database
from sqlalchemy.orm import (
    mapped_column,
    relationship,
    Mapped,
)
from datetime import datetime


# Model for the PlayerState table
class PlayerState(Database.Base):
    __tablename__ = "PlayerState"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("Player.id"))
    game_id: Mapped[int] = mapped_column(ForeignKey("Game.id"))
    state: Mapped[str] = mapped_column(String, nullable=False)
    rec_score: Mapped[int] = mapped_column(Integer, nullable=False)
    heart_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Relations
    player: Mapped["Player"] = relationship("Player", back_populates="states")
    game: Mapped["Game"] = relationship("Game", back_populates="states")

    def __repr__(self) -> str:
        return f"<PlayerState(player_id={self.player_id}, game_id={self.game_id}, state={self.state}, timestamp={self.timestamp})>"
