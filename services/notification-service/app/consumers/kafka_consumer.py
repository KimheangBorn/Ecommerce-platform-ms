import json
import logging
from aiokafka import AIOKafkaConsumer
from app.config import settings
from app.services.email_service import email_service
import asyncio

logger = logging.getLogger(__name__)

class NotificationConsumer:
    def __init__(self):
        self.consumer = None
        self.running = False

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            'order-created', 'payment-success',
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id='notification-service-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        await self.consumer.start()
        self.running = True
        logger.info("Notification Consumer Started")
        
        try:
            async for message in self.consumer:
                if not self.running: break
                
                try:
                    topic = message.topic
                    data = message.value
                    
                    if topic == 'order-created':
                        # In a real app, user email would come from User Service or be part of event
                        # Here assuming it's in event or using a mock
                        user_email = data.get('user_email', 'customer@example.com')
                        await email_service.send_order_confirmation(
                            to=user_email,
                            order_number=data.get('order_id'), # or order_number field
                            items=data.get('items', []),
                            total=data.get('total_amount', 0)
                        )
                    
                    elif topic == 'payment-success':
                        logger.info(f"Payment success notification for Order {data.get('order_id')}")
                        
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    
        finally:
            await self.consumer.stop()

    async def stop(self):
        self.running = False
        if self.consumer:
            await self.consumer.stop()

notification_consumer = NotificationConsumer()
