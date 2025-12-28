from flask import Blueprint, jsonify, request
from app import db
from app.models.inventory import Inventory, inventory_schema
from app.services.inventory_service import InventoryService

bp = Blueprint('inventory', __name__)

@bp.route('/<int:product_id>', methods=['GET'])
def get_inventory(product_id):
    inventory = Inventory.query.filter_by(product_id=product_id).first_or_404()
    return jsonify(inventory_schema.dump(inventory)), 200

@bp.route('/adjust', methods=['POST'])
def adjust_inventory():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    
    # Simple adjustment (add stock)
    inventory = Inventory.query.filter_by(product_id=product_id).first()
    if not inventory:
        inventory = Inventory(product_id=product_id, total_quantity=0, available_quantity=0)
        db.session.add(inventory)
    
    inventory.total_quantity += quantity
    inventory.available_quantity += quantity
    
    db.session.commit()
    
    return jsonify(inventory_schema.dump(inventory)), 200
