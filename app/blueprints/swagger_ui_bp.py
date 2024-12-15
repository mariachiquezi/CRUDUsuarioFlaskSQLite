from flask import Blueprint
from flask_restx import Api

swagger_bp = Blueprint('swagger', __name__)
api = Api(swagger_bp, doc='/swagger-ui/')

def register_swagger_ui(app):
    app.register_blueprint(swagger_bp, url_prefix='/')
