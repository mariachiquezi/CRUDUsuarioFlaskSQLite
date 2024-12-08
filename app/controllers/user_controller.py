from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.exceptions.exception_handler import ExceptionHandler
from app.exceptions.validation_error import ValidationError, UniqueConstraintError

# Define o blueprint para agrupar as rotas de usuário
user_bp = Blueprint("user", __name__)


# Rota para criar um novo usuário
@user_bp.route("/usuarios", methods=["POST"])
def create_user():
    try:
        data = request.json
        response, status_code = UserService().create_user(data)
        return jsonify(response), status_code
    except ValidationError as e:
        # Erro de validação (como CPF ou Email inválido)
        return ExceptionHandler.handle_validation_error(e)
    except UniqueConstraintError as e:
        # Erro de violação de unicidade (CPF ou Email já existe)
        return ExceptionHandler.handle_unique_constraint_error(e)
    except Exception as e:
        # Erro genérico não tratado
        return ExceptionHandler.handle_generic_error(e)


# Rota para listar todos os usuários
@user_bp.route("/usuarios", methods=["GET"])
def list_users():
    try:
        response = UserService().list_users()
        return jsonify(response)
    except Exception as e:
        # Erro genérico no serviço de usuários
        return ExceptionHandler.handle_generic_error(e)


# Rota para obter um único usuário pelo ID
@user_bp.route("/usuarios/<string:id>", methods=["GET"])
def get_user(id):
    try:
        response, status_code = UserService().get_user(id)
        return jsonify(response), status_code
    except Exception as e:
        # Erro genérico ao buscar o usuário
        return ExceptionHandler.handle_generic_error(e)


# Rota para atualizar um usuário existente
@user_bp.route("/usuarios/<string:id>", methods=["PUT"])
def update_user(id):
    try:
        data = request.json
        response, status_code = UserService().update_user(id, data)
        return jsonify(response), status_code
    except ValidationError as e:
        return ExceptionHandler.handle_validation_error(e)
    except UniqueConstraintError as e:
        return ExceptionHandler.handle_unique_constraint_error(e)
    except Exception as e:
        return ExceptionHandler.handle_generic_error(e)


# Rota para deletar um usuário
@user_bp.route("/usuarios/<string:id>", methods=["DELETE"])
def delete_user(id):
    try:
        response, status_code = UserService().delete_user(id)
        return jsonify(response), status_code
    except Exception as e:
        return ExceptionHandler.handle_generic_error(e)
