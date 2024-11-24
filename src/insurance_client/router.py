
from fastapi import APIRouter, HTTPException

from src.insurance_client.client import  RateService

router = APIRouter(prefix="/rates", tags=["rates"])

from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas
from .kafka_file import send_to_kafka


@router.post("/tariffs/", response_model=schemas.TariffResponse)
async def create_tariff(
    tariff: schemas.TariffCreate,
):
    return await RateService.create_rate(data=tariff.dict())


@router.post("/tariffs/by_date/", response_model=dict)
async def create_tariffs_by_date(
    tariffs_by_date: schemas.TariffsByDateCreate,
):
    await RateService.create_rates_by_date(data=tariffs_by_date.dict())
    return {"message": "Tariffs created successfully"}


@router.get("/tariffs/", response_model=list[schemas.TariffResponse])
async def read_tariffs():
    tariffs = await RateService.get_all_rates()
    return tariffs


@router.delete("/tariffs/{tariff_id}", response_model=schemas.TariffResponse)
async def delete_tariff(tariff_id: int,):
    deleted = await RateService.delete_rate(rate_id=tariff_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tariff not found")
    return deleted


@router.put("/tariffs/{tariff_id}", response_model=schemas.TariffResponse)
async def update_tariff(
    tariff_id: int, tariff: schemas.TariffUpdate,
):
    updated = await RateService.update_rate(rate_id=tariff_id, data=tariff.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Tariff not found")
    return updated


@router.get("/tariffs/by_date/", response_model=dict)
async def get_tariffs_structured( ):
    tariffs = await RateService.get_all_rates()
    structured_tariffs = {}

    for tariff in tariffs:
        date_str = tariff["effective_date"].isoformat()
        if date_str not in structured_tariffs:
            structured_tariffs[date_str] = []

        structured_tariffs[date_str].append({
            "cargo_type": tariff["cargo_type"],
            "rate": tariff["rate"],
            "effective_date": date_str,
        })

    return structured_tariffs


@router.post("/insurance/", response_model=schemas.InsuranceResponse)
async def calculate_insurance(
    insurance_request: schemas.InsuranceRequest,

):
    insurance_cost = await RateService.calculate_insurance_cost(
        cargo_type=insurance_request.cargo_type,
        declared_value=insurance_request.declared_value,
        effective_date=insurance_request.effective_date
    )

    if insurance_cost == 0.0:
        raise HTTPException(status_code=404, detail="Tariff not found for the given cargo type and date")

    return schemas.InsuranceResponse(
        cargo_type=insurance_request.cargo_type,
        declared_value=insurance_request.declared_value,
        insurance_cost=insurance_cost
    )