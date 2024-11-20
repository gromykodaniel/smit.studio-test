import datetime
from pathlib import Path

from fastapi import APIRouter, Query

from src.insurance_client.client import RateClient
from src.insurance_client.models import Rate
from src.insurance_client.schemas import TariffRateInsert, Rates

router = APIRouter(prefix="/rates", tags=["rates"])


@router.post("/date",status_code=200)
def tariff_rate_date(
    data: Rates,
):
    data = RateClient.insert(json=True, **data.model_dump())
    return {}


@router.get("/calculate", status_code=200)
def tariff_calculate(
    cargo_type: str = Query(),
    declared_price: float = Query(),
    date: datetime.date = Query(),

):
    data = RateClient.calculate(
        cargo_type=cargo_type, date=date, declared_price=declared_price
    )
    return {}