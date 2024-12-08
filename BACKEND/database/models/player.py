from database.database import Database
from sqlalchemy import String, DateTime, Integer, ForeignKey
import typing
from sqlalchemy.orm import (
    mapped_column,
    relationship,
    Mapped,
)
from datetime import datetime

# Model for the Player table
class Player(Database.Base):
    __tablename__ = "Player"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("Team.id"))
    line_id: Mapped[int] = mapped_column(ForeignKey("Line.id"), nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    birth_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    position: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[typing.Optional[str]] = mapped_column(String, unique=True, nullable=True)
    number: Mapped[int] = mapped_column(Integer, nullable=True)

    # Relations
    team: Mapped["Team"] = relationship("Team", back_populates="players")
    line: Mapped["Line"] = relationship("Line", back_populates="players")
    medical_data: Mapped[typing.List["GameMedicalData"]] = relationship("GameMedicalData", back_populates="player")
    states: Mapped[typing.List["PlayerState"]] = relationship("PlayerState", back_populates="player")
    player_device_at: Mapped[typing.List["PlayerDeviceAt"]] = relationship("PlayerDeviceAt", back_populates="player")

    def __repr__(self) -> str:
        return (f"<Player(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, "
                f"team_id={self.team_id}, line_id={self.line_id}, birth_date={self.birth_date}, "
                f"position={self.position}, email={self.email}, number={self.number})>")

