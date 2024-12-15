from flask import Flask
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from app.config import Config
from db import db
from app.limiter import limiter
from app.blueprints.user_blueprints import user_bp
from app.exceptions.error_handler import register_error_handlers

# Inicialize o Marshmallow antes da função create_app
ma = Marshmallow()


def create_app():
    app = Flask(__name__)

    # Configurações do aplicativo
    app.config.from_object(Config)

    # Inicializa extensões
    db.init_app(app)
    Migrate(app, db)
    register_error_handlers(app)
    ma.init_app(app)  # Inicializa o Marshmallow

    # Adicione a sessão do SQLAlchemy ao Marshmallow
    with app.app_context():
        ma.SQLAlchemySchema.Meta.session = db.session

    # Registra Blueprints
    app.register_blueprint(user_bp)

    # Inicializa o Flask-Limiter após os Blueprints
    limiter.init_app(app)

    return app
