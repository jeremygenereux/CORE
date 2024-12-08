from database.database import Database
from sqlalchemy import String
import hashlib
import typing
from sqlalchemy.orm import (
    mapped_column,
    relationship,
    Mapped,
)

# Model for the Coach table
class Coach(Database.Base):
    __tablename__ = "Coach"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    # Relations
    teams: Mapped[typing.List["Team"]] = relationship("Team", back_populates="coach")

    def __init__(self, first_name: str, last_name: str, email: str, password: str):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)

    def set_password(self, password: str) -> None:
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def __repr__(self) -> str:
        return f"<Coach(first_name={self.first_name}, last_name={self.last_name}, email={self.email})>"
