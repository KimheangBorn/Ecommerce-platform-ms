import logging
import json
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import redis
from app.config import settings

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.template_env = Environment(loader=FileSystemLoader('app/templates'))
        self.redis = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )

    async def send_order_confirmation(self, to: str, order_number: str, items: list, total: float):
        template = self.template_env.get_template('order_confirmation.html')
        content = template.render(
            order_number=order_number,
            items=items,
            total=total
        )
        
        # Simulate sending
        logger.info(f"--------------------------------------------------")
        logger.info(f"[EMAIL SIMULATION] To: {to}")
        logger.info(f"Subject: Order Confirmation #{order_number}")
        logger.info(f"Body: {content}")
        logger.info(f"--------------------------------------------------")
        
        # Log to Redis
        self.log_notification(order_number, 'EMAIL', to)

    def log_notification(self, reference_id, type, recipient):
        key = f"notification:{reference_id}"
        data = {
            "type": type,
            "recipient": recipient,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.redis.lpush(key, json.dumps(data))
        self.redis.expire(key, 2592000) # 30 days

email_service = EmailService()
