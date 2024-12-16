from flask import Blueprint, request, jsonify
from flask_restx import Resource, Namespace, fields
from app.controllers.user_controller import UserController
from app.limiter import limiter
from app.schemas.user_schema import user_schema, users_schema
from app.utils.clean_user_data import clean_user_data
import json

user_bp = Blueprint("user", __name__)
api = Namespace("Users", description="Operações relacionadas aos usuários")

user_model = api.model(
    "User",
    {
        "name": fields.String(required=True, description="Nome do usuário"),
        "cpf": fields.String(required=True, description="CPF do usuário"),
        "email": fields.String(required=True, description="Email do usuário"),
        "birth_date": fields.String(
            required=True, description="Data de nascimento do usuário"
        ),
        "password_hash": fields.String(required=True, description="Senha do usuário"),
    },
)


@api.route("/")
class UserList(Resource):
    @api.doc("list_users")
    @limiter.limit("5 per minute")
    def get(self):
        """Lista todos os usuários"""
        response, status_code = UserController.list_users()
        if status_code == 200:
            users_data = response.get("users", [])
            return users_data, status_code
        else:
            return response, status_code

    @api.expect(user_model)
    @api.doc("create_user")
    @limiter.limit(
        "5 per minute",
        error_message="Limite de requisições excedido. Por favor, aguarde e tente novamente em breve.",
    )
    def post(self):
        """Cria um novo usuário"""
        data = request.json
        data = clean_user_data(data)
        try:
            user_data = user_schema.load(data)
            user_data_dict = user_schema.dump(user_data)
        except Exception as e:
            return jsonify({"error": str(e)}), 400

        response, status_code = UserController.create_user(user_data_dict)
        return response, status_code


@api.route("/<string:id>")
@api.response(404, "Usuário não encontrado")
class User(Resource):
    @api.doc("get_user")
    @limiter.limit("5 per minute")
    def get(self, id):
        """Obtém um usuário pelo ID"""
        response, status_code = UserController.get_user(id)
        if status_code == 200:
            user_data = response.get("user", {})
            return user_data, status_code
        else:
            return response, status_code

    @api.expect(user_model)
    @api.doc("update_user")
    @limiter.limit(
        "3 per minute",
        error_message="Limite de requisições excedido. Por favor, aguarde e tente novamente em breve.",
    )
    def put(self, id):
        """Atualiza um usuário existente"""
        data = request.json
        data = clean_user_data(data)
        updated_data = user_schema.load(data, partial=True)
        response, status_code = UserController.update_user(id, updated_data)
        return response, status_code

    @api.doc("delete_user")
    @limiter.limit(
        "5 per minute",
        error_message="Limite de requisições excedido. Por favor, aguarde e tente novamente em breve.",
    )
    def delete(self, id):
        """Deleta um usuário"""
        response, status_code = UserController.delete_user(id)
        return response, status_code
