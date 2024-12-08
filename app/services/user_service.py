from app.exceptions.exception_handler import ExceptionHandler
from app.exceptions.validation_error import UniqueConstraintError, ValidationError
from app.repositories.user_repository import UserRepository
from app.services.users_validator.birth_validator_service import BirthFormatter
from app.services.users_validator.user_data_validator_service import (
    UserDataValidatorService,
)
from app.utils.id_generator import generate_unique_id
from app.utils.format import format_cpf, get_current_timestamp
import db
from sqlalchemy.exc import SQLAlchemyError


class UserService:
    def __init__(self):
        self.repository = UserRepository()
        self.validation_service = UserDataValidatorService()
        self.format_date = BirthFormatter()
        self.generate_unique_id = generate_unique_id
        self.error_handler = ExceptionHandler()

    def create_user(self, data):
        try:
            # Validação e preparação dos dados
            user_data = self._validate_and_prepare_user_data(data)

            # Salvar usuário
            self.repository.create_user(user_data)
            return {"message": "Usuário criado com sucesso!"}, 201

        except (ValidationError, UniqueConstraintError, SQLAlchemyError) as e:
            return self.error_handler.handle_database_error(e)
        except Exception as e:
            return self.error_handler.handle_generic_error(e)

    def update_user(self, user_id, data):
        try:
            # Validação e preparação dos dados
            user_data = self._validate_and_prepare_user_data(data, user_id)

            # Atualizar usuário
            self.repository.update_user(user_data)
            return {"message": "Usuário atualizado com sucesso!"}, 200

        except (ValidationError, Exception) as e:
            db.session.rollback()
            return self.error_handler.handle_generic_error(e)

    def get_user(self, user_id):
        try:
            # Buscar e formatar o usuário
            user = self.repository.get_user_by_id(user_id)
            if user is None:
                return {"error": "Usuário não encontrado."}, 404

            user["cpf"] = format_cpf(user["cpf"])
            return user, 200

        except Exception as e:
            return self.error_handler.handle_generic_error(e)

    def list_users(self):
        try:
            # Listar usuários e formatar CPF
            users = self.repository.list_users()
            for user in users:
                user["cpf"] = format_cpf(user["cpf"])

            return users, 200

        except Exception as e:
            return self.error_handler.handle_generic_error(e)

    def delete_user(self, user_id):
        try:
            # Verificar se o usuário existe
            user = self.repository.get_user_by_id(user_id)
            if user is None:
                return {"error": "Usuário não encontrado."}, 404

            # Deletar usuário
            self.repository.delete_user(user_id)
            return {"message": "Usuário deletado com sucesso!"}, 200

        except Exception as e:
            db.session.rollback()
            return self.error_handler.handle_generic_error(e)

    def _validate_and_prepare_user_data(self, data, user_id=None):
        """
        Valida os dados do usuário e prepara os dados para criação ou atualização.
        """
        password_hash, formatted_cpf, formatted_birth_date, valid = (
            self._validate_user_data(data)
        )
        if not valid:
            raise ValidationError("Dados do usuário inválidos.")

        # Prepara os dados ajustados
        return self._prepare_user_data(
            data, password_hash, formatted_cpf, formatted_birth_date, user_id
        )

    def _validate_user_data(self, data):
        """
        Valida os dados do usuário e retorna as informações formatadas.
        """
        return self.validation_service.validate(
            data["email"], data["password_hash"], data["cpf"], data["birth_date"]
        )

    def _prepare_user_data(
        self, data, password_hash, formatted_cpf, formatted_birth_date, user_id=None
    ):
        """
        Prepara os dados do usuário, incluindo o formato da data e geração do ID.
        """
        # Não altere diretamente o parâmetro data, crie uma cópia
        user_data = data.copy()

        user_data["password_hash"] = password_hash
        user_data["cpf"] = formatted_cpf
        user_data["birth_date"] = formatted_birth_date
        user_data["id"] = user_id or self.generate_unique_id(data["cpf"])
        user_data["time_created"] = get_current_timestamp()  # Ajuste do timestamp
        user_data["time_updated"] = get_current_timestamp()

        return user_data
