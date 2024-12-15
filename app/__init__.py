from flask import Flask
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_restx import Api
from app.config import Config
from db import db
from app.limiter import limiter
from app.blueprints.user_blueprints import user_bp, api as user_api_namespace
from app.exceptions.error_handler import register_error_handlers
from app.blueprints.swagger_ui_bp import register_swagger_ui

ma = Marshmallow()


def create_app():
    app = Flask(__name__)

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

    register_swagger_ui(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
