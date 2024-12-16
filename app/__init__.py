import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_restx import Api
from app.config import Config
from app.limiter import limiter
from db import db
from app.resources.user_resource import user_bp, api as user_api_namespace
from app.exceptions.error_handler import register_error_handlers

ma = Marshmallow()


def create_app():
    app = Flask(__name__)

    if not app.debug:
        handler = RotatingFileHandler("app.log", maxBytes=10000, backupCount=3)
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)

    app.config.from_object(Config)

    api = Api(app, version="1.0", title="Users", description="CRUD de Usuários")

    # Inicializa extensões
    db.init_app(app)
    Migrate(app, db)
    register_error_handlers(app)
    ma.init_app(app)

    with app.app_context():
        ma.SQLAlchemySchema.Meta.session = db.session

    app.register_blueprint(user_bp, url_prefix="/api")
    api.add_namespace(user_api_namespace, path="/api/users")

    limiter.init_app(app)

    return app
