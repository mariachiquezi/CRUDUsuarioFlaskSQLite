from app.constants import COLUMN_NAMES
from app.exceptions.database_error import UniqueConstraintError
from app.exceptions.validation_error import ValidationError
from app.repositories.user_repository import UserRepository
from app.services.users_validator.user_data_validator_service import (
    UserDataValidatorService,
)
from app.services.users_validator.validation_service.validation_service import (
    prepare_user_data,
    validate_data,
)
from app.utils.id_generator import generate_unique_id
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.error_handler import ErrorHandler


class UserService:
    def __init__(self):
        self.generate_unique_id = generate_unique_id

    def create_user(self, data):
        print("creadteeeeee")
        """Cria um novo usuário com base nos dados recebidos."""
        data["id"] = None
        return self._save_user(data, "create")

    def update_user(self, user_id, data):
        """Atualiza um usuário existente com base no ID e dados fornecidos."""
        data["id"] = user_id  # Passa o user_id para o update
        return self._save_user(data, "update")

    def get_user(self, user_id):
        """Obtém os dados de um usuário pelo ID."""
        try:
            user = UserRepository.get_user(user_id)
            if user:

                user_dict = dict(zip(COLUMN_NAMES, user))

                return {"user": user_dict}, 200
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    def list_users(self):
        """Lista os dados de todos os usuários."""
        try:
            users = UserRepository.list_users()
            if users:
                print("users", users)
                # Converte a lista de objetos do modelo UserModel para dicionários
                return {"users": [user for user in users]}, 200
            return {"message": "Nenhum usuário encontrado"}, 404
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    def delete_user(self, user_id):
        """Deleta um usuário pelo ID."""
        try:
            user = UserRepository.get_user(user_id)
            if user:
                UserRepository.delete_user(user_id)
                return {"message": "Usuário excluído com sucesso!"}, 200
            return {"message": "Usuário não encontrado"}, 404
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    def _save_user(self, data, action):
        """
        Função genérica para salvar ou atualizar um usuário.

        :param data: Dados do usuário.
        :param action: Ação que será realizada - 'create' ou 'update'.
        """
        try:
            # Valida e prepara os dados
            validated_data = validate_data(data)
            user_data = prepare_user_data(validated_data, data.get("id"))
            # Salva ou atualiza no banco de dados
            if action == "create":
                UserRepository.create_user(user_data)
                return {"message": "Usuário criado com sucesso!"}, 201
            elif action == "update":
                UserRepository.update_user(user_data)
                return {"message": "Usuário atualizado com sucesso!"}, 200

        except (UniqueConstraintError, SQLAlchemyError) as e:
            return ErrorHandler.handle_database_error(e)
        except ValidationError as e:  # Captura erros de validação
            return {"error": str(e)}, 400
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)
