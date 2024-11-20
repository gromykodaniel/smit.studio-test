from datetime import date, datetime
from datetime import date

from sqlalchemy import Column, Date,DateTime, Integer, UniqueConstraint, func
from src.database import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped
from src.database import Base


class Rate(Base):
    __tablename__ = "rate"

    id: Mapped[int] = mapped_column(primary_key=True)
    cargo_type : Mapped[str]
    on_date : Mapped[date] = mapped_column(Date)
    rate : Mapped[float]

    date_create: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
