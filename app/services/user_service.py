import logging
from app.constants import COLUMN_NAMES, REQUIRED_FIELDS
from app.exceptions.database_error import MissingFieldError, UniqueConstraintError
from app.exceptions.validation_error import ValidationError
from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository
from app.utils.format_cpf import format_cpf
from app.exceptions.error_handler import ErrorHandler
from app.utils.format_date import get_current_timestamp
from app.utils.users_validators.prepare_user import (
    extract_updated_fields,
    validate_and_prepare_data,
)
from app.utils.users_validators.validations_users import (
    convert_to_dict,
    get_existing_user,
    prepare_data_for_save,
    validate_duplicate_fields,
)

# Configuração básica do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserService:

    def create_user(self, data):
        try:
            logger.info("Iniciando criação de usuário.")
            data = prepare_data_for_save(data)
            validated_data = validate_and_prepare_data(data, "create")
            user = UserRepository.create_user(validated_data)
            logger.info("Usuário criado com sucesso.")
            return {"message": "Usuário criado com sucesso!"}, 201
        except (
            ValidationError,
            UniqueConstraintError,
            MissingFieldError,
            ValueError,
        ) as e:
            logger.error(f"Erro ao criar usuário: {str(e)}")
            return {"error": str(e)}, 400
        except Exception as e:
            logger.error(f"Erro genérico ao criar usuário: {str(e)}")
            return ErrorHandler.handle_generic_error(e)

    def update_user(self, user_id, data):
        try:
            logger.info(f"Iniciando atualização do usuário com ID: {user_id}")
            data = prepare_data_for_save(data, user_id)
            existing_user = get_existing_user(user_id)
            if not existing_user:
                logger.warning(f"Usuário com ID {user_id} não encontrado.")
                return {"message": "Usuário não encontrado"}, 404

            updated_fields = extract_updated_fields(
                data, dict(zip(COLUMN_NAMES, existing_user))
            )
            if not updated_fields:
                logger.info("Nenhuma alteração detectada.")
                return {"message": "Nenhuma alteração detectada."}, 400

            validate_duplicate_fields(updated_fields, user_id)
            validated_data = validate_and_prepare_data(updated_fields, "update")
            validated_data["id"] = user_id
            validated_data["time_updated"] = get_current_timestamp()

            UserRepository.update_user(validated_data)
            logger.info(f"Usuário com ID {user_id} atualizado com sucesso.")
            return {"message": "Usuário atualizado com sucesso!"}, 200
        except (
            ValidationError,
            UniqueConstraintError,
            MissingFieldError,
            ValueError,
        ) as e:
            logger.error(f"Erro ao atualizar usuário: {str(e)}")
            return {"error": str(e)}, 400
        except Exception as e:
            logger.error(f"Erro genérico ao atualizar usuário: {str(e)}")
            return ErrorHandler.handle_generic_error(e)

    def get_user(self, user_id):
        try:
            logger.info(f"Buscando usuário com ID: {user_id}")
            user = UserRepository.get_user(user_id)
            if user:
                user_dict = dict(user)
                user_dict["cpf"] = format_cpf(user_dict["cpf"])
                logger.info(f"Usuário com ID {user_id} encontrado.")
                return {"user": user_dict}, 200
            logger.warning(f"Usuário com ID {user_id} não encontrado.")
            return {"message": "Usuário não encontrado"}, 404
        except Exception as e:
            logger.error(f"Erro genérico ao buscar usuário: {str(e)}")
            return ErrorHandler.handle_generic_error(e)

    def list_users(self):
        try:
            logger.info("Listando todos os usuários.")
            users = UserRepository.list_users()
            if users:
                formatted_users = [
                    {**dict(user), "cpf": format_cpf(user["cpf"])} for user in users
                ]
                logger.info(f"{len(formatted_users)} usuário(s) encontrado(s).")
                return {"users": formatted_users}, 200
            logger.info("Nenhum usuário encontrado.")
            return {"message": "Nenhum usuário encontrado"}, 404
        except Exception as e:
            logger.error(f"Erro genérico ao listar usuários: {str(e)}")
            return ErrorHandler.handle_generic_error(e)

    def delete_user(self, user_id):
        try:
            logger.info(f"Deletando usuário com ID: {user_id}")
            if UserRepository.get_user(user_id):
                UserRepository.delete_user(user_id)
                logger.info(f"Usuário com ID {user_id} deletado com sucesso.")
                return {"message": "Usuário deletado com sucesso!"}, 200
            logger.warning(f"Usuário com ID {user_id} não encontrado.")
            return {"message": "Usuário não encontrado"}, 404
        except Exception as e:
            logger.error(f"Erro genérico ao deletar usuário: {str(e)}")
            return ErrorHandler.handle_generic_error(e)
