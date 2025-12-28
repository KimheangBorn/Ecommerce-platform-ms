from flask import Blueprint, request, jsonify
from app import db
from app.models.product import Product, product_schema, products_schema
from app.utils.cache import get_cache, set_cache, delete_cache_pattern
from sqlalchemy import or_

bp = Blueprint('products', __name__)

@bp.route('', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Try cache first
    cache_key = f'products:page:{page}:limit:{per_page}'
    cached_data = get_cache(cache_key)
    if cached_data:
        return jsonify(cached_data), 200

    # DB Query
    pagination = Product.query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    result = {
        'products': products_schema.dump(pagination.items),
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }
    
    # Set cache (5 minutes)
    set_cache(cache_key, result, 300)
    
    return jsonify(result), 200

@bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    # Try cache
    cache_key = f'product:{id}'
    cached_data = get_cache(cache_key)
    if cached_data:
        return jsonify(cached_data), 200

    product = Product.query.get_or_404(id)
    result = product_schema.dump(product)
    
    # Set cache (1 hour)
    set_cache(cache_key, result, 3600)
    
    return jsonify(result), 200

@bp.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])

    products = Product.query.filter(
        or_(
            Product.name.ilike(f'%{query}%'),
            Product.description.ilike(f'%{query}%'),
            Product.sku.ilike(f'%{query}%')
        )
    ).all()
    
    return jsonify(products_schema.dump(products)), 200

@bp.route('', methods=['POST'])
def create_product():
    data = request.get_json()
    try:
        new_product = Product(
            sku=data['sku'],
            name=data['name'],
            description=data.get('description'),
            price=data['price'],
            category_id=data.get('category_id'),
            is_active=data.get('is_active', True)
        )
        db.session.add(new_product)
        db.session.commit()
        
        # Invalidate list cache
        delete_cache_pattern('products:page:*')
        
        return jsonify(product_schema.dump(new_product)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    
    try:
        if 'name' in data: product.name = data['name']
        if 'description' in data: product.description = data['description']
        if 'price' in data: product.price = data['price']
        if 'category_id' in data: product.category_id = data['category_id']
        if 'is_active' in data: product.is_active = data['is_active']
        
        db.session.commit()
        
        # Invalidate specific cache and list cache
        delete_cache_pattern(f'product:{id}')
        delete_cache_pattern('products:page:*')
        
        return jsonify(product_schema.dump(product)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    
    try:
        db.session.delete(product)
        db.session.commit()
        
        # Invalidate caches
        delete_cache_pattern(f'product:{id}')
        delete_cache_pattern('products:page:*')
        
        return jsonify({'message': 'Product deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
