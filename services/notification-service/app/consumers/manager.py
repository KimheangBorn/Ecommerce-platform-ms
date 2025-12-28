from app.consumers.kafka_consumer import notification_consumer

async def start_consumers_task():
    await notification_consumer.start()

async def stop_consumers_task():
    await notification_consumer.stop()
