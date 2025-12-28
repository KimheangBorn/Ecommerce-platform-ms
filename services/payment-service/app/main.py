from fastapi import FastAPI
from app.routes import payments, health
from app.database import engine, Base

app = FastAPI(title="Payment Service")

from app.services.kafka_producer import kafka_producer

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await kafka_producer.start()

@app.on_event("shutdown")
async def shutdown():
    await kafka_producer.stop()

app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(payments.router, prefix="/api/payments", tags=["Payments"])
