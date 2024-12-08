from database.database import Database
from sqlalchemy import Integer, Boolean, ForeignKey
from sqlalchemy.orm import (
    mapped_column,
    relationship,
    Mapped,
)
import typing

# Model for the Line table
class Line(Database.Base):
    __tablename__ = "Line"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("Team.id"), nullable=False)
    is_offense: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    line_number: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relations
    team: Mapped["Team"] = relationship("Team", back_populates="lines")
    players: Mapped[typing.List["Player"]] = relationship("Player", back_populates="line")

    def __repr__(self) -> str:
        return f"<Line(team_id={self.team_id}, line_number={self.line_number}, is_offense={self.is_offense})>"