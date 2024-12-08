from database.database import Database
from sqlalchemy import (
    ForeignKey,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import (
    mapped_column,
    relationship,
    Mapped,
)
from datetime import datetime
import typing

# Model for the Game table
class Game(Database.Base):
    __tablename__ = "Game"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("Team.id"))
    start_ts: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_ts: Mapped[typing.Optional[datetime]] = mapped_column(DateTime)
    is_underway: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relations
    team: Mapped["Team"] = relationship("Team", back_populates="games")
    heart_rate_data: Mapped[typing.List["HeartRateData"]] = relationship("HeartRateData", back_populates="game")
    states: Mapped[typing.List["PlayerState"]] = relationship("PlayerState", back_populates="game")

    def __repr__(self) -> str:
        return f"<Game(team_id={self.team_id}, start_ts={self.start_ts}, is_underway={self.is_underway})>"
