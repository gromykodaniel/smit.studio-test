from typing import Union

from fastapi import FastAPI

from src.insurance_client.router import router

app = FastAPI()


app.add_route(router)