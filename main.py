

from fastapi import FastAPI
from aiokafka import AIOKafkaProducer

from src.insurance_client.router import router

app = FastAPI()


app.include_router(router)





producer = None
@app.on_event("startup")
async def startup_event():

    global producer

    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()
@app.on_event("shutdown")
async def shutdown_event():

    await producer.stop()
