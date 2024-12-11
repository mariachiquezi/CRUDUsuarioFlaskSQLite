from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.exceptions.error_handler import ErrorHandler
from app.exceptions.validation_error import ValidationError
from app.exceptions.database_error import UniqueConstraintError
from app.limiter import limiter

# Inicializando o Limiter diretamente para esse Blueprint

# Define o blueprint para agrupar as rotas de usuário
user_bp = Blueprint("user", __name__)


# Função de tratamento de erro para reduzir repetição
def handle_request(func):
    """
    Wrapper para tratar erros de forma centralizada nas rotas.
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except UniqueConstraintError as e:
            return ErrorHandler.handle_unique_constraint_error(e)
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    return wrapper


# Rota para criar um novo usuário (limitação de 5 requisições por minuto)
@user_bp.route("/usuarios", methods=["POST"], endpoint="create_user")
@limiter.limit("5 per minute")
@handle_request
def create_user():
    """
    Cria um novo usuário com base nas informações fornecidas na requisição.
    Aplica limitação de requisições e trata erros específicos.
    """
    data = request.json
    response, status_code = UserService().create_user(data)
    return jsonify(response), status_code


# Rota para listar todos os usuários (limitação de 10 requisições por hora)
@user_bp.route("/usuarios", methods=["GET"], endpoint="list_users")
@limiter.limit("5 per minute", error_message="Muitas requisições para listar usuários! Aguarde 1 minuto e tente novamente.")
@handle_request
def list_users():
    """
    Lista todos os usuários registrados.
    Aplica limitação de requisições e trata erros específicos.
    """
    response = UserService().list_users()
    return jsonify(response)


# Rota para obter um único usuário pelo ID (limitação de 5 requisições por minuto)
@user_bp.route("/usuarios/<string:id>", methods=["GET"], endpoint="get_user")
@limiter.limit("10 per minute", error_message="Você está tentando acessar informações de usuários muito rapidamente! Espere um momento.")
@handle_request
def get_user(id):
    """
    Obtém as informações de um usuário específico pelo seu ID.
    Aplica limitação de requisições e trata erros específicos.
    """
    response, status_code = UserService().get_user(id)
    return jsonify(response), status_code


# Rota para atualizar um usuário existente (limitação de 3 requisições por minuto)
@user_bp.route("/usuarios/<string:id>", methods=["PUT"], endpoint="update_user")
@limiter.limit("2 per minute", error_message="Muitas requisições para atualizar usuários! Aguarde 1 minuto.")
@handle_request
def update_user(id):
    """
    Atualiza as informações de um usuário específico.
    Aplica limitação de requisições e trata erros específicos.
    """
    data = request.json
    response, status_code = UserService().update_user(id, data)
    return jsonify(response), status_code


# Rota para deletar um usuário (limitação de 2 requisições por minuto)
@user_bp.route("/usuarios/<string:id>", methods=["DELETE"], endpoint="delete_user")
@limiter.limit("2 per minute", error_message="Você excedeu o limite para deletar usuários. Tente novamente em 1 minuto.")
@handle_request
def delete_user(id):
    """
    Deleta um usuário com base no ID fornecido.
    Aplica limitação de requisições e trata erros específicos.
    """
    response, status_code = UserService().delete_user(id)
    return jsonify(response), status_code
