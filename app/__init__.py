import os
from flask import Flask
from flask_migrate import Migrate
from db import db
from app.config import Config
from app.controllers.user_controller import user_bp


def create_app():
    app = Flask(__name__)

    # Configuração do banco de dados
    app.config.from_object(Config)

    # Inicializa extensões
    db.init_app(app)
    Migrate(app, db)

    # Registro dos Blueprints
    app.register_blueprint(user_bp)

    return app
