from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Rate(Base):
    __tablename__ = "rate"

    id = Column(Integer, primary_key=True, index=True)
    cargo_type = Column(String, index=True)
    rate = Column(Float, nullable=False)
    effective_date = Column(Date, nullable=False)

    tariff_group_id = Column(Integer)

