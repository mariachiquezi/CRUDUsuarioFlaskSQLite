from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

# Define o blueprint para agrupar as rotas de usuário
user_bp = Blueprint("user", __name__)


# Rota para criar um novo usuário
@user_bp.route("/usuarios", methods=["POST"])
def criar_usuario():
    data = request.json
    response, status_code = UserService().criar_usuario(data)
    return jsonify(response), status_code


# Rota para listar todos os usuários
@user_bp.route("/usuarios", methods=["GET"])
def list_users():
    response = UserService().list_users()
    return jsonify(response)


# Rota para obter um único usuário pelo ID
@user_bp.route("/usuarios/<string:id>", methods=["GET"])
def get_user(id):
    response, status_code = UserService().get_user(id)
    return jsonify(response), status_code


# Rota para atualizar um usuário existente
@user_bp.route("/usuarios/<string:id>", methods=["PUT"])
def update_user(id):
    data = request.json
    response, status_code = UserService().update_user(id, data)
    return jsonify(response), status_code


# Rota para deletar um usuário
@user_bp.route("/usuarios/<string:id>", methods=["DELETE"])
def delete_user(id):
    response, status_code = UserService().delete_user(id)
    return jsonify(response), status_code
