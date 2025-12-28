from flask import Blueprint, request, jsonify
from app import db
from app.models.category import Category, category_schema, categories_schema
from sqlalchemy.exc import IntegrityError

bp = Blueprint('categories', __name__)

@bp.route('', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify(categories_schema.dump(categories)), 200

@bp.route('', methods=['POST'])
def create_category():
    data = request.get_json()
    try:
        new_category = Category(
            name=data['name'],
            description=data.get('description')
        )
        db.session.add(new_category)
        db.session.commit()
        return jsonify(category_schema.dump(new_category)), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Category name already exists'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get_or_404(id)
    return jsonify(category_schema.dump(category)), 200

@bp.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category deleted'}), 200
