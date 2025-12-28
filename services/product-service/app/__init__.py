from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from app.config import config
import os

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
        
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # Import routes
    from app.routes import products, categories, health
    app.register_blueprint(products.bp, url_prefix='/api/products')
    app.register_blueprint(categories.bp, url_prefix='/api/categories')
    app.register_blueprint(health.bp, url_prefix='/health')

    return app
