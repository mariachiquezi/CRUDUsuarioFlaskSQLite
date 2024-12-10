from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.config import Config
from db import db
from flask_migrate import Migrate
from app.controllers.user_controller import user_bp
from app.exceptions.error_handler import register_error_handlers

limiter = Limiter(get_remote_address, app=None)


def create_app():
    app = Flask(__name__)

    # Configuração do banco de dados
    app.config.from_object(Config)

    # Inicializa as extensões
    db.init_app(app)
    Migrate(app, db)
    register_error_handlers(app)

    # Inicializa o Flask-Limiter
    limiter.init_app(app)

    # Registro dos Blueprints
    app.register_blueprint(user_bp)

    return app
