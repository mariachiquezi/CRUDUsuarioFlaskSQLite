import logging
from flask import Blueprint, request, jsonify
from flask_restx import Resource, Namespace, fields
from marshmallow.exceptions import ValidationError as MarshmallowValidationError
from app.controllers.user_controller import UserController
from app.exceptions.error_handler import ErrorHandler
from app.limiter import limiter
from app.schemas.user_schema import user_schema
from app.utils.clean_user_data import clean_user_data

# Configuração básica do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        try:
            logger.info("Requisição para listar todos os usuários recebida.")
            response, status_code = UserController.list_users()
            if status_code == 200:
                users_data = response.get("users", [])
                logger.info("Usuários listados com sucesso.")
                return users_data, status_code
            else:
                logger.warning("Nenhum usuário encontrado.")
                return response, status_code
        except Exception as e:
            logger.error(f"Erro ao listar usuários: {str(e)}")
            return ErrorHandler.handle_generic_error(e)

    @api.expect(user_model)
    @api.doc("create_user")
    @limiter.limit(
        "5 per minute",
        error_message="Limite de requisições excedido. Por favor, aguarde e tente novamente em breve.",
    )
    def post(self):
        """Cria um novo usuário"""
        try:
            data = request.json
            logger.info("Requisição para criar usuário recebida.")
            data = clean_user_data(data)
            logger.info(f"Dados após limpeza: {data}")
            user_data = user_schema.load(data)
            user_data_dict = user_schema.dump(user_data)
            response, status_code = UserController.create_user(user_data_dict)
            logger.info("Usuário criado com sucesso.")
            return response, status_code
        except MarshmallowValidationError as e:
            logger.error(f"Erro de validação: {e.messages}")
            return {"error": e.messages}, 400
        except Exception as e:
            logger.error(f"Erro ao criar usuário: {str(e)}")
            return ErrorHandler.handle_generic_error(e)


@api.route("/<string:id>")
@api.response(404, "Usuário não encontrado")
class User(Resource):
    @api.doc("get_user")
    @limiter.limit("5 per minute")
    def get(self, id):
        """Obtém um usuário pelo ID"""
        try:
            logger.info(f"Requisição para obter usuário com ID: {id} recebida.")
            response, status_code = UserController.get_user(id)
            if status_code == 200:
                user_data = response.get("user", {})
                logger.info(f"Usuário com ID: {id} encontrado.")
                return user_data, status_code
            else:
                logger.warning(f"Usuário com ID: {id} não encontrado.")
                return response, status_code
        except Exception as e:
            logger.error(f"Erro ao obter usuário: {str(e)}")
            return ErrorHandler.handle_generic_error(e)

    @api.expect(user_model)
    @api.doc("update_user")
    @limiter.limit(
        "3 per minute",
        error_message="Limite de requisições excedido. Por favor, aguarde e tente novamente em breve.",
    )
    def put(self, id):
        """Atualiza um usuário existente"""
        try:
            data = request.json
            logger.info(f"Requisição para atualizar usuário com ID: {id} recebida.")
            data = clean_user_data(data)
            logger.info(f"Dados após limpeza: {data}")
            updated_data = user_schema.load(data, partial=True)
            response, status_code = UserController.update_user(id, updated_data)
            logger.info(f"Usuário com ID: {id} atualizado com sucesso.")
            return response, status_code
        except MarshmallowValidationError as e:
            logger.error(f"Erro de validação: {e.messages}")
            return jsonify({"error": e.messages}), 400
        except Exception as e:
            logger.error(f"Erro ao atualizar usuário: {str(e)}")
            return ErrorHandler.handle_generic_error(e)

    @api.doc("delete_user")
    @limiter.limit(
        "5 per minute",
        error_message="Limite de requisições excedido. Por favor, aguarde e tente novamente em breve.",
    )
    def delete(self, id):
        """Deleta um usuário"""
        try:
            logger.info(f"Requisição para deletar usuário com ID: {id} recebida.")
            response, status_code = UserController.delete_user(id)
            logger.info(f"Usuário com ID: {id} deletado com sucesso.")
            return response, status_code
        except Exception as e:
            logger.error(f"Erro ao deletar usuário: {str(e)}")
            return ErrorHandler.handle_generic_error(e)
