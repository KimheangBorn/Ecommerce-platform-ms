import json
import logging
from kafka import KafkaConsumer
from app.config import Config
from app import create_app
from app.services.inventory_service import InventoryService, InsufficientStockError

logger = logging.getLogger(__name__)

class OrderConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'order-created',
            bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
            group_id='inventory-service-group',
            auto_offset_reset='earliest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

    def start(self):
        # Create app context for DB access
        app = create_app()
        with app.app_context():
            logger.info("Starting Order Consumer...")
            for message in self.consumer:
                try:
                    data = message.value
                    order_id = data.get('order_id')
                    items = data.get('items', [])
                    
                    logger.info(f"Processing order-created for Order {order_id}")
                    
                    InventoryService.reserve_stocks(order_id, items)
                    
                    logger.info(f"Stock reserved for Order {order_id}")
                    
                except InsufficientStockError as e:
                    logger.error(f"Insufficient stock for Order {order_id}: {e}")
                    # TODO: Publish 'order-rejected' or 'stock-unavailable' event
                except Exception as e:
                    logger.error(f"Error processing order {order_id}: {e}")
