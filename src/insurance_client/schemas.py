import datetime

from pydantic import BaseModel, Extra, Field


from pydantic import BaseModel, Field
from typing import List, Dict

class RateItem(BaseModel):
    cargo_type: str = Field(..., )
    rate: float = Field(..., ge=0)

class Rates(BaseModel):
    __root__: Dict[str, List[RateItem]]

    class Config:
        schema_extra = {
            "example": {
                "2020-01-01": [
                    {"cargo_type": "glass", "rate": 0.06},
                    {"cargo_type": "other", "rate": 0.01},
                ],
                "2020-07-01": [
                    {"cargo_type": "glass", "rate": 0.035},
                    {"cargo_type": "other", "rate": 0.015},
                ],
            }
        }





class TariffRateInsert(BaseModel, extra=Extra.allow):
    pass


class TariffRateDate(BaseModel):
    date: datetime.date = Field(description="Дата")