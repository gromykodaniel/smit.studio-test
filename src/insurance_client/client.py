from sqlalchemy import  insert, select
from fastapi import HTTPException
from select import select

from src.database import async_session_maker
from src.insurance_client.models import Rate


class RateClient:
    def __init__(self, json: bool = False, **kwargs):
        if json:
            self._parse_param(**kwargs)
            return
        self.__dict__.update(kwargs)

    def _parse_param(self, **kv):
        result = []
        for date, v in kv.items():
            for rate in v:
                rate.update(on_date=date)
                result.append(rate)
        self.values = result

    async  def insert(self):
        if not self.values:
            raise Exception("Initialize object with param json=True")
        print(self.values)
        stmt = insert(Rate).values(self.values).returning(*[col for col in Rate.__table__.c])
        async with async_session_maker() as session:
            result = await session.execute(stmt)
            await session.commit()
            return result

    async def calculate(self):

        async with async_session_maker() as session:
            result = await Rate.execute(select(func.max(Rate.on_date)))
            if not result:
                raise HTTPException(
                    status_code=400, detail="Tariff for that date not set"
                )
            rate = await session.execute(
                select(Rate)
                .where(
                    Rate.Tariff.cargo_type == self.cargo_type,
                    Rate.Tariff.on_date == max_date,
                )
            )
            rate = rate.scalar_one_or_none()
            if not rate:
                raise HTTPException(
                    status_code=404, detail="Tariff with that cargo type not found"
                )
            return {"total_amount": self.declared_price * float(rate.rate)}