from fastapi import FastAPI
from app.routes import health
from app.consumers.manager import start_consumers_task, stop_consumers_task
import asyncio

app = FastAPI(title="Notification Service")

@app.on_event("startup")
async def startup():
    # Start consumers as an asyncio task
    asyncio.create_task(start_consumers_task())

@app.on_event("shutdown")
async def shutdown():
    await stop_consumers_task()

app.include_router(health.router, prefix="/health", tags=["Health"])
