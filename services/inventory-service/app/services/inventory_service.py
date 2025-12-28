from app import db
from app.models.inventory import Inventory, Reservation
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

class InsufficientStockError(Exception):
    pass

class InventoryService:
    
    @staticmethod
    def reserve_stocks(order_id, items):
        """
        Items: list of dict {'product_id': 1, 'quantity': 2}
        """
        # Start transaction
        try:
            reservations = []
            
            # Sort items by product_id to prevent deadlocks
            items.sort(key=lambda x: x['product_id'])
            
            for item in items:
                p_id = item['product_id']
                qty = item['quantity']
                
                # Pessimistic Lock: SELECT FOR UPDATE
                inventory = Inventory.query.filter_by(product_id=p_id).with_for_update().first()
                
                if not inventory:
                    # Should probably create it or raise error. For now assume inventory exists.
                    raise InsufficientStockError(f"Product {p_id} not found in inventory")
                
                if inventory.available_quantity < qty:
                    raise InsufficientStockError(f"Insufficient stock for product {p_id}")
                
                # Update inventory
                inventory.available_quantity -= qty
                inventory.reserved_quantity += qty
                
                # Create reservation
                res = Reservation(
                    order_id=order_id,
                    product_id=p_id,
                    quantity=qty,
                    expires_at=datetime.utcnow() + timedelta(minutes=15)
                )
                db.session.add(res)
                reservations.append(res)
            
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def confirm_reservation(order_id):
        try:
            reservations = Reservation.query.filter_by(order_id=order_id, status='RESERVED').all()
            if not reservations:
                return
            
            for res in reservations:
                res.status = 'CONFIRMED'
                # Stock is already deducted from available, just moved to reserved.
                # When confirmed, we effectively remove it from reserved 'pool' concept if we tracked sold, 
                # but our model tracks Total, Avail, Reserved. 
                # So: Total -= Qty, Reserved -= Qty.
                
                inventory = Inventory.query.filter_by(product_id=res.product_id).with_for_update().first()
                if inventory:
                    inventory.total_quantity -= res.quantity
                    inventory.reserved_quantity -= res.quantity
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error confirming reservation: {e}")

    @staticmethod
    def release_reservation(order_id):
        try:
            reservations = Reservation.query.filter_by(order_id=order_id, status='RESERVED').all()
            if not reservations:
                return
            
            for res in reservations:
                res.status = 'CANCELLED'
                
                inventory = Inventory.query.filter_by(product_id=res.product_id).with_for_update().first()
                if inventory:
                    inventory.available_quantity += res.quantity
                    inventory.reserved_quantity -= res.quantity
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error releasing reservation: {e}")
