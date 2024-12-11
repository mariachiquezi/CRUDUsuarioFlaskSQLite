from flask import Flask
from flask_migrate import Migrate
from app.config import Config
from db import db
from app.limiter import limiter
from app.controllers.user_controller import user_bp
from app.exceptions.error_handler import register_error_handlers


def create_app():
    app = Flask(__name__)

    # Configurações do aplicativo
    app.config.from_object(Config)

    # Inicializa extensões
    db.init_app(app)
    Migrate(app, db)
    register_error_handlers(app)

    # Registra Blueprints
    app.register_blueprint(user_bp)

    # Inicializa o Flask-Limiter após os Blueprints
    limiter.init_app(app)

    return app
