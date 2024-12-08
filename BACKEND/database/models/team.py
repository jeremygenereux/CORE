from database.database import Database
from sqlalchemy import String, ForeignKey
import typing
from sqlalchemy.orm import (
    mapped_column,
    relationship,
    Mapped,
)

# Model for the Team table
class Team(Database.Base):
    __tablename__ = "Team"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    coach_id: Mapped[int] = mapped_column(ForeignKey("Coach.id"))
    team_name: Mapped[str] = mapped_column(String, nullable=False)
    primary_color: Mapped[str] = mapped_column(String, nullable=False)
    secondary_color: Mapped[str] = mapped_column(String, nullable=False)
    logo: Mapped[typing.Optional[str]] = mapped_column(String)
    description: Mapped[typing.Optional[str]] = mapped_column(String)

    # Relations
    coach: Mapped["Coach"] = relationship("Coach", back_populates="teams")
    players: Mapped[typing.List["Player"]] = relationship("Player", back_populates="team")
    lines: Mapped[typing.List["Line"]] = relationship("Line", back_populates="team")
    games: Mapped[typing.List["Game"]] = relationship("Game", back_populates="team")

    def __repr__(self) -> str:
        return f"<Team(team_name={self.team_name}, coach_id={self.coach_id})>"
