
from pydantic import BaseModel , Field
from datetime import date
from typing import List


class TariffCreate(BaseModel):
    cargo_type: str = Field(..., description="Тип груза")
    rate: float = Field(..., ge=0, description="Тариф за единицу груза")
    effective_date: date = Field(..., description="Дата вступления тарифа в силу")


class TariffUpdate(BaseModel):
    cargo_type: str = Field(..., description="Тип груза", min_length=1)
    rate: float = Field(..., ge=0, description="Тариф за единицу груза")
    effective_date: date = Field(..., description="Дата вступления тарифа в силу")


class TariffResponse(TariffCreate):
    id: int

    class Config:
        orm_mode = True


class TariffsByDateResponse(BaseModel):
    tariffs_by_date: dict[date, List[TariffCreate]]

    class Config:
        orm_mode = True


class TariffsByDateCreate(BaseModel):
    tariffs_by_date: dict[date, List[TariffCreate]]



    class Config:
        orm_mode = True
