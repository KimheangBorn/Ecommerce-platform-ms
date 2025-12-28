from aiokafka import AIOKafkaProducer
from app.config import settings
import json
import asyncio

class KafkaProducer:
    def __init__(self):
        self.producer = None
    
    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')
        )
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()
    
    async def publish(self, topic: str, message: dict):
        if not self.producer:
            await self.start()
        try:
            await self.producer.send_and_wait(topic, message)
        except Exception as e:
            print(f"Error publishing to Kafka: {e}")
            # In production, might want to retry or circuit break
            pass

kafka_producer = KafkaProducer()
