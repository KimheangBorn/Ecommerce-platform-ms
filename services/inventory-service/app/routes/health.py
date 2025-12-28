from flask import Blueprint, jsonify
from app import db

bp = Blueprint('health', __name__)

@bp.route('/live', methods=['GET'])
def liveness():
    return jsonify({'status': 'UP'}), 200

@bp.route('/ready', methods=['GET'])
def readiness():
    try:
        db.session.execute('SELECT 1')
        return jsonify({'status': 'UP', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'DOWN', 'error': 'Database disconnected'}), 503
