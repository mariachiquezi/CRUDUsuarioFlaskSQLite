# app/services/user_service.py
from datetime import datetime
from sqlite3 import DatabaseError
from app.exceptions.exception_handler import ExceptionHandler
from app.exceptions.validation_error import UniqueConstraintError, ValidationError
from app.services.users_validator.birth_validator_service import BirthFormatter
from app.services.users_validator.user_data_validator_service import (
    UserDataValidatorService,
)
from app.repositories.user_repository import UserRepository
from app.utils.id_generator import generate_unique_id
from db import db
from app.models.user_model import UserModel
from sqlalchemy.exc import SQLAlchemyError


class UserService:
    def __init__(self):
        self.repository = UserRepository()
        self.validation_service = UserDataValidatorService()
        self.format_date = BirthFormatter()
        self.generate_unique_id = generate_unique_id
        self.error = ExceptionHandler()

    def create_user(self, data):
        try:
            # Validar dados do usuário (delegado para ValidatorService)
            password_hash, formatted_cpf, formatted_birth_date, valid = (
                self.validation_service.validate(
                    data["email"],
                    data["password_hash"],
                    data["cpf"],
                    data["birth_date"],
                )
            )
            if not valid:
                raise ValidationError("Dados do usuário inválidos.")

            # Criar o objeto de usuário (delegado para método privado)
            self._create_user_object(
                data, password_hash, formatted_cpf, formatted_birth_date
            )
            data["time_created"] = data.get(
                "time_created", datetime.utcnow()
            )  # Data de criação
            data["time_updated"] = data.get("time_updated", datetime.utcnow())
            # Salvar no banco de dados (delegado para o repositório)
            query = self.repository.create_user()
            self.repository.save_to_db(query, data)

            return {"message": "Usuário criado com sucesso!"}, 201
        except ValidationError as e:
            # Tratar erro de validação
            return ExceptionHandler.handle_validation_error(e)

        except UniqueConstraintError as e:  # Se você tiver exceções personalizadas
            # Tratar violação de chave única
            return ExceptionHandler.handle_unique_constraint_error(e)

        except SQLAlchemyError as e:  # Exemplo de erro genérico relacionado ao banco
            # Tratar erro de banco de dados
            return ExceptionHandler.handle_database_error(e)

        except Exception as e:
            # Tratar qualquer outro erro genérico
            return ExceptionHandler.handle_generic_error(e)

    def update_user(self, user_id, data):
        try:
            # Validar dados do usuário (delegado para ValidatorService)
            password_hash, formatted_cpf, valid = self.validation_service.validate(
                data["email"], data["password_hash"], data["cpf"], data["birth_date"]
            )
            if not valid:
                raise ValidationError("Dados do usuário inválidos.")

            # Criar o objeto de usuário (delegado para método privado)
            updated_user = self._create_user_object(data, password_hash, formatted_cpf)

            # Atualizar no banco de dados (delegado para o repositório)
            query = self.repository.update_user()
            data["id"] = user_id  # Adicionar o ID do usuário ao dicionário
            self.repository.save_to_db(query, data)

            return {"message": "Usuário atualizado com sucesso!"}, 200

        except ValidationError as e:
            return ExceptionHandler.handle_validation_error(e)

        except Exception as e:
            db.session.rollback()
            return ExceptionHandler.handle_generic_error(e)

    def get_user(self, user_id):
        try:
            # Buscar usuário no banco de dados
            query = self.repository.get_user()
            result = db.session.execute(query, {"id": user_id}).fetchone()

            if result is None:
                return {"error": "Usuário não encontrado."}, 404

            # Converter o resultado para um dicionário
            user = dict(result._mapping)

            # Formatar CPF antes de retornar
            user["cpf"] = self.validation_service.run(user["cpf"])

            return user, 200

        except Exception as e:
            return ExceptionHandler.handle_generic_error(e)

    def delete_user(self, user_id):
        try:
            # Verificar se o usuário existe
            query = self.repository.get_user()
            result = db.session.execute(query, {"id": user_id}).fetchone()

            if result is None:
                return {"error": "Usuário não encontrado."}, 404

            # Deletar o usuário
            query = self.repository.delete_user()
            self.repository.save_to_db(query, {"id": user_id})

            return {"message": "Usuário deletado com sucesso!"}, 200

        except Exception as e:
            db.session.rollback()
            return ExceptionHandler.handle_generic_error(e)

    def _create_user_object(
        self, data, password_hash, formatted_cpf, formatted_birth_date
    ):
        # Preparar o objeto de usuário antes de salvar
        data["id"] = self.generate_unique_id(data["cpf"])
        data["password_hash"] = password_hash
        data["cpf"] = formatted_cpf
        data["formatted_birth_date"] = self.format_date.format_date_for_db(
            formatted_birth_date
        )
        return UserModel(**data)

    def list_users(self):
        try:
            query = self.repository.list_users()
            result = db.session.execute(query).fetchall()
            # Converter o resultado para um dicionário
            users = [dict(row._mapping) for row in result]

            # Formatar CPF antes de retornar
            for user in users:
                user["cpf"] = self.validation_service.format_cpf(user["cpf"])

            return users, 200

        except Exception as e:
            return ExceptionHandler.handle_generic_error(e)
