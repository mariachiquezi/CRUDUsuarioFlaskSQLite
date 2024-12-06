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
def listar_usuarios():
    response = UserService().listar_usuarios()
    return jsonify(response)


# Rota para obter um único usuário pelo ID
@user_bp.route("/usuarios/<int:id>", methods=["GET"])
def obter_usuario(id):
    response, status_code = UserService().obter_usuario(id)
    return jsonify(response), status_code


# Rota para atualizar um usuário existente
@user_bp.route("/usuarios/<int:id>", methods=["PUT"])
def atualizar_usuario(id):
    data = request.json
    response, status_code = UserService().atualizar_usuario(id, data)
    return jsonify(response), status_code


# Rota para deletar um usuário
@user_bp.route("/usuarios/<int:id>", methods=["DELETE"])
def deletar_usuario(id):
    response, status_code = UserService().deletar_usuario(id)
    return jsonify(response), status_code
