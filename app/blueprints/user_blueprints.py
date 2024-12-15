from flask import Blueprint, request, jsonify
from app.controllers.user_controller import UserController
from app.limiter import limiter
from app.schemas.user_schema import user_schema, users_schema
import json

user_bp = Blueprint("user", __name__)


from app.utils.clean_user_data import clean_user_data


@user_bp.route("/users", methods=["POST"], endpoint="create_user")
@limiter.limit(
    "5 per minute",
    error_message="Limite de requisições excedido. Por favor, aguarde e tente novamente em breve.",
)
def create_user():
    data = request.json
    data = clean_user_data(data)
    print("Dados recebidos:", data)

    try:
        user_data = user_schema.load(data)
        print("Dados do usuário carregados:", user_data)
    except Exception as e:
        print("Erro ao carregar os dados do usuário:", str(e))
        return jsonify({"error": str(e)}), 400
    print("mandando pra create")
    response, status_code = UserController.create_user(user_data)
    return jsonify(response), status_code


@user_bp.route("/users", methods=["GET"], endpoint="list_users")
@limiter.limit(
    "5 per minute",
    error_message="Limite de requisições excedido. Por favor, aguarde e tente novamente em breve.",
)
def list_users():
    response, status_code = UserController.list_users()
    print("Response:", response)
    print("Status code:", status_code)

    if status_code == 200:
        users_data = response.get("users", [])
        print("Users data:", users_data)
        return jsonify(users_data), status_code
    else:
        return jsonify(response), status_code


@user_bp.route("/users/<string:id>", methods=["GET"], endpoint="get_user")
@limiter.limit(
    "10 per minute",
    error_message="Limite de requisições excedido. Por favor, aguarde e tente novamente em breve.",
)
def get_user(id):
    response, status_code = UserController.get_user(id)
    print("Response:", response)
    print("Status code:", status_code)

    if status_code == 200:
        user_data = response.get("user", {})
        print("User data:", user_data)
        return jsonify(user_data), status_code
    else:
        return jsonify(response), status_code


@user_bp.route("/users/<string:id>", methods=["PUT"], endpoint="update_user")
@limiter.limit(
    "3 per minute",
    error_message="Limite de requisições excedido. Por favor, aguarde e tente novamente em breve.",
)
def update_user(id):
    data = request.json
    data = clean_user_data(data)
    updated_data = user_schema.load(data, partial=True)
    response, status_code = UserController.update_user(id, updated_data)
    return jsonify(response), status_code


@user_bp.route("/users/<string:id>", methods=["DELETE"], endpoint="delete_user")
@limiter.limit(
    "5 per minute",
    error_message="Limite de requisições excedido. Por favor, aguarde e tente novamente em breve.",
)
def delete_user(id):
    response, status_code = UserController.delete_user(id)
    return jsonify(response), status_code
