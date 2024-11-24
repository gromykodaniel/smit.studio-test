from main import producer
from src.database import async_session_maker
from fastapi import HTTPException
from sqlalchemy import insert, select, update, delete
from datetime import date
from typing import Optional, Dict, List
from . import models


class RateService:

    @staticmethod
    async def create_rate(data: dict, user_id: Optional[int] = None) -> Optional[dict]:
        query = insert(models.Rate).values(**data).returning(models.Rate.id)
        async with async_session_maker() as session:
            try:
                result = await session.execute(query)
                await session.commit()
                rate_id = result.mappings().first()

                if rate_id:
                    message = {
                        "user_id": user_id,
                        "action": "create_rate",
                        **data,
                        "id": rate_id["id"],
                        "timestamp": data["effective_date"].isoformat(),
                    }
                    await producer.send_and_wait("test_topic",message)

                return rate_id
            except Exception as e:
                raise HTTPException(status_code=404)

    @staticmethod
    async def get_rate(rate_id: int) -> Optional[dict]:
        query = select(models.Rate).where(models.Rate.id == rate_id)
        async with async_session_maker() as session:
            result = await session.execute(query)
            rate = result.mappings().first()
            if not rate:


                raise HTTPException(status_code=404)

            return rate

    @staticmethod
    async def get_all_rates() -> List[dict]:
        query = select(models.Rate)
        async with async_session_maker() as session:
            result = await session.execute(query)
            return result.mappings().all()

    @staticmethod
    async def delete_rate(rate_id: int, user_id: Optional[int] = None) -> Optional[dict]:
        async with async_session_maker() as session:
            try:
                query = delete(models.Rate).where(models.Rate.id == rate_id).returning(
                    models.Rate.id, models.Rate.cargo_type, models.Rate.rate, models.Rate.effective_date
                )
                result = await session.execute(query)
                await session.commit()
                rate = result.mappings().first()

                if rate:
                    message = {
                        "user_id": user_id,
                        "action": "delete_rate",
                        **rate,
                        "timestamp": rate["effective_date"].isoformat(),
                    }
                    await producer.send_and_wait("test_topic",message)

                return rate
            except Exception as e:

                raise HTTPException(status_code=404)

    @staticmethod
    async def update_rate(rate_id: int, data: dict, user_id: Optional[int] = None) -> Optional[dict]:
        async with async_session_maker() as session:
            try:
                query = (
                    update(models.Rate)
                    .where(models.Rate.id == rate_id)
                    .values(**data)
                    .returning(
                        models.Rate.id,
                        models.Rate.cargo_type,
                        models.Rate.rate,
                        models.Rate.effective_date,
                    )
                )
                result = await session.execute(query)
                await session.commit()
                updated_rate = result.mappings().first()

                if updated_rate:
                    message = {
                        "user_id": user_id,
                        "action": "update_rate",
                        **updated_rate,
                        "timestamp": updated_rate["effective_date"].isoformat(),
                    }
                    await producer.send_and_wait("test_topic",message)

                return updated_rate
            except Exception as e:

                raise HTTPException(status_code=404)

    @staticmethod
    async def create_rates_by_date(data: dict, user_id: Optional[int] = None):
        async with async_session_maker() as session:
            try:
                rates_to_create = []
                for effective_date, rates in data.items():
                    for rate in rates:
                        rate_data = {**rate, "effective_date": effective_date}
                        rates_to_create.append(rate_data)

                query = insert(models.Rate).values(rates_to_create).returning(models.Rate.id)
                result = await session.execute(query)
                await session.commit()

                rate_ids = result.mappings().all()

                for rate_data in rates_to_create:
                    message = {
                        "user_id": user_id,
                        "action": "create_rate",
                        **rate_data,
                        "timestamp": rate_data["effective_date"].isoformat(),
                    }
                    await producer.send_and_wait("test_topic",message)

                return rate_ids
            except Exception as e:
                await session.rollback()
                raise HTTPException(status_code=404)

    @staticmethod
    async def get_rates_by_date(effective_date: date) -> Dict[date, List[dict]]:
        query = select(models.Rate).where(models.Rate.effective_date == effective_date)
        async with async_session_maker() as session:
            result = await session.execute(query)
            rates = result.mappings().all()
            if not rates:
                raise HTTPException(status_code=404)

            return {effective_date: rates}
