import json
import logging
from kafka import KafkaConsumer
from app.config import Config
from app import create_app
from app.services.inventory_service import InventoryService

logger = logging.getLogger(__name__)

class PaymentConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'payment-success', 'payment-failed',
            bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
            group_id='inventory-service-group',
            auto_offset_reset='earliest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

    def start(self):
        app = create_app()
        with app.app_context():
            logger.info("Starting Payment Consumer...")
            for message in self.consumer:
                try:
                    topic = message.topic
                    data = message.value
                    order_id = data.get('order_id')
                    
                    if topic == 'payment-success':
                        logger.info(f"Processing payment-success for Order {order_id}")
                        InventoryService.confirm_reservation(order_id)
                        logger.info(f"Reservation confirmed for Order {order_id}")
                        
                    elif topic == 'payment-failed':
                        logger.info(f"Processing payment-failed for Order {order_id}")
                        InventoryService.release_reservation(order_id)
                        logger.info(f"Reservation released for Order {order_id}")
                        
                except Exception as e:
                    logger.error(f"Error processing payment event for order {order_id}: {e}")
