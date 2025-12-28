from flask import Blueprint, jsonify
from app import db
import redis
from app.config import Config

bp = Blueprint('health', __name__)

@bp.route('/live', methods=['GET'])
def liveness():
    return jsonify({'status': 'UP'}), 200

@bp.route('/ready', methods=['GET'])
def readiness():
    # Check DB
    try:
        db.session.execute('SELECT 1')
        db_status = 'connected'
    except Exception as e:
        return jsonify({'status': 'DOWN', 'error': 'Database disconnected'}), 503

    # Check Redis
    try:
        r = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_DB, socket_timeout=1)
        r.ping()
        redis_status = 'connected'
    except Exception as e:
        return jsonify({'status': 'DOWN', 'error': 'Redis disconnected'}), 503

    return jsonify({
        'status': 'UP',
        'database': db_status,
        'redis': redis_status
    }), 200
