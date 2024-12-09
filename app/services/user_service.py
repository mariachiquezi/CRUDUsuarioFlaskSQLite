# app/services/user_service.py
from app.exceptions.exception_handler import ExceptionHandler
from app.exceptions.validation_error import UniqueConstraintError, ValidationError
from app.repositories.user_repository import UserRepository
from app.services.users_validator.birth_validator_service import BirthFormatter
from app.services.users_validator.user_data_validator_service import (
    UserDataValidatorService,
)
from app.utils.id_generator import generate_unique_id
from app.utils.format import format_cpf, get_current_timestamp
from app.schemas.user_schema import UserSchema
from sqlalchemy.exc import SQLAlchemyError


class UserService:
    def __init__(self):
        self.repository = UserRepository()
        self.validation_service = UserDataValidatorService()
        self.format_date = BirthFormatter()
        self.generate_unique_id = generate_unique_id
        self.error_handler = ExceptionHandler()

    def create_user(self, data):
        """Cria um novo usuário com base nos dados recebidos."""
        return self._save_user(data, "create")

    def update_user(self, user_id, data):
        """Atualiza um usuário existente com base no ID e dados fornecidos."""
        data["id"] = user_id  # Passa o user_id para o update
        return self._save_user(data, "update")

    def get_user_by_id(self, user_id):
        """Obtém os dados de um usuário pelo ID."""
        try:
            user = self.repository.get_user_by_id(user_id)
            if user:
                return {"user": user}, 200
            return {"message": "Usuário não encontrado"}, 404
        except Exception as e:
            return self.error_handler.handle_generic_error(e)

    def list_users(self):
        """Obtém os dados de um usuário pelo CPF."""
        try:
            user = self.repository.list_users()
            if user:
                return {"user": user}, 200
            return {"message": "Usuário não encontrado"}, 404
        except Exception as e:
            return self.error_handler.handle_generic_error(e)

    def delete_user(self, user_id):
        """Deleta um usuário pelo ID."""
        try:
            user = self.repository.get_user_by_id(user_id)
            if user:
                self.repository.delete_user(user_id)
                return {"message": "Usuário excluído com sucesso!"}, 200
            return {"message": "Usuário não encontrado"}, 404
        except Exception as e:
            return self.error_handler.handle_generic_error(e)

    def _save_user(self, data, action):
        """
        Função genérica para salvar ou atualizar um usuário.

        :param data: Dados do usuário.
        :param action: Ação que será realizada - 'create' ou 'update'.
        """
        try:
            # Valida e prepara os dados
            validated_data = self._validate_data(data)
            user_data = self._prepare_user_data(validated_data, data.get("id"))

            # Salva ou atualiza no banco de dados
            if action == "create":
                self.repository.create_user(user_data)
                return {"message": "Usuário criado com sucesso!"}, 201
            elif action == "update":
                self.repository.update_user(user_data)
                return {"message": "Usuário atualizado com sucesso!"}, 200

        except (ValidationError, UniqueConstraintError, SQLAlchemyError) as e:
            return self.error_handler.handle_database_error(e)
        except Exception as e:
            return self.error_handler.handle_generic_error(e)

    def _validate_data(self, data):
        """Valida os dados do usuário utilizando o schema."""
        try:
            validated_data = UserSchema(**data)  # Valida com o schema
            return (
                validated_data.dict()
            )  # Retorna os dados validados como um dicionário
        except Exception as e:
            raise ValidationError(f"Erro de validação: {str(e)}")

    def _prepare_user_data(self, validated_data, user_id=None):
        """
        Prepara os dados do usuário para criação ou atualização.
        """
        password_hash, formatted_cpf, formatted_birth_date, valid = (
            self._validate_user_data(validated_data)
        )
        if not valid:
            raise ValidationError("Dados do usuário inválidos.")

        user_data = validated_data.copy()
        user_data["password_hash"] = password_hash
        user_data["name"] = user_data["name"]
        user_data["cpf"] = formatted_cpf
        user_data["birth_date"] = formatted_birth_date
        user_data["id"] = user_id or self.generate_unique_id(validated_data["cpf"])
        user_data["time_created"] = get_current_timestamp()  # Ajuste do timestamp
        user_data["time_updated"] = get_current_timestamp()

        return user_data

    def _validate_user_data(self, data):
        """
        Valida os dados do usuário e retorna as informações formatadas.
        """
        return self.validation_service.validate(
            data["email"], data["password_hash"], data["cpf"], data["birth_date"]
        )
