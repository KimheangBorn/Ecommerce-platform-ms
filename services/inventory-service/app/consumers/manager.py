import threading
from app.consumers.order_consumer import OrderConsumer
from app.consumers.payment_consumer import PaymentConsumer

def run_order_consumer():
    consumer = OrderConsumer()
    consumer.start()

def run_payment_consumer():
    consumer = PaymentConsumer()
    consumer.start()

def start_consumers_in_thread(app):
    # This is a simple way to run consumers for this demo/MVP.
    # In production, run these as separate commands (e.g. python -m app.consumers.order_consumer)
    
    t1 = threading.Thread(target=run_order_consumer)
    t1.daemon = True
    t1.start()
    
    t2 = threading.Thread(target=run_payment_consumer)
    t2.daemon = True
    t2.start()
