from flask import Blueprint
from app.controllers.user_controller import UserController
from app.limiter import limiter

# Define o blueprint para agrupar as rotas de usuário
user_bp = Blueprint("user", __name__)


# Rota para criar um novo usuário (limitação de 5 requisições por minuto)
@user_bp.route("/users", methods=["POST"], endpoint="create_user")
@limiter.limit(
    "5 per minute",
    error_message="Limite de requisições excedido. Por favor, aguarde e tente novamente em breve.",
)
def create_user():
    return UserController.create_user()


# Rota para listar todos os usuários (limitação de 5 requisições por hora)
@user_bp.route("/users", methods=["GET"], endpoint="list_users")
@limiter.limit(
    "5 per minute",
    error_message="Limite de requisições excedido. Por favor, aguarde e tente novamente em breve.",
)
def list_users():
    return UserController.list_users()


# Rota para obter um único usuário pelo ID (limitação de 10 requisições por minuto)
@user_bp.route("/users/<string:id>", methods=["GET"], endpoint="get_user")
@limiter.limit(
    "10 per minute",
    error_message="Limite de requisições excedido. Por favor, aguarde e tente novamente em breve.",
)
def get_user(id):
    return UserController.get_user(id)


# Rota para atualizar um usuário existente (limitação de 3 requisições por minuto)
@user_bp.route("/users/<string:id>", methods=["PUT"], endpoint="update_user")
@limiter.limit(
    "3 per minute",
    error_message="Limite de requisições excedido. Por favor, aguarde e tente novamente em breve.",
)
def update_user(id):
    return UserController.update_user(id)


# Rota para deletar um usuário (limitação de 6 requisições por minuto)
@user_bp.route("/users/<string:id>", methods=["DELETE"], endpoint="delete_user")
@limiter.limit(
    "5 per minute",
    error_message="Limite de requisições excedido. Por favor, aguarde e tente novamente em breve.",
)
def delete_user(id):
    return UserController.delete_user(id)
