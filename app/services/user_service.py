from app.constants import COLUMN_NAMES, REQUIRED_FIELDS
from app.exceptions.database_error import (
    DatabaseError,
    MissingFieldError,
    UniqueConstraintError,
)
from app.exceptions.validation_error import ValidationError
from app.repositories.user_repository import UserRepository
from app.utils.validations_users import (
    extract_updated_fields,
    validate_and_prepare_data,
    validate_duplicate_fields,
)
from app.utils.format_cpf import format_cpf
from app.exceptions.error_handler import ErrorHandler
from app.utils.format_date import get_current_timestamp
from app.services.users_validator.password_validator_service import PasswordService


class UserService:
    def create_user(self, data):
        try:
            print("data", data)
            for field in REQUIRED_FIELDS:
                if field not in data or not data[field]:
                    raise MissingFieldError(field)

            data["id"] = None
            # Validar duplicatas para criação
            validate_duplicate_fields(data)
            validated_data = validate_and_prepare_data(data, "create")

            user = UserRepository.create_user(validated_data)
            print("foi aq ")
            print("user", user)
            print("user", user)
            return {"message": "Usuário criado com sucesso!"}, 201
        except ValidationError as e:
            return {"error": str(e)}, 400
        except (UniqueConstraintError, MissingFieldError) as e:
            return {"error": str(e)}, 400
        except ValueError as e:
            # Capturar ValueError especificamente
            return {"error": str(e)}, 400
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    def get_existing_user(self, user_id):
        existing_user = UserRepository.get_user(user_id)
        print("oi")
        if not existing_user:
            return None
        return existing_user

    def update_user(self, user_id, data):
        try:
            existing_user = self.get_existing_user(user_id)
            print("sim exite", existing_user)
            if not existing_user:
                print("nao existe")
                return {
                    "message": "Usuário não encontrado"
                }, 404  # Retorna mensagem de usuário não encontrado

            updated_fields = extract_updated_fields(
                data, dict(zip(COLUMN_NAMES, existing_user))
            )
            if not updated_fields:
                return {"message": "Nenhuma alteração detectada."}, 400

            validate_duplicate_fields(updated_fields, user_id)
            validated_data = validate_and_prepare_data(updated_fields, "update")
            validated_data["id"] = user_id
            validated_data["time_updated"] = get_current_timestamp()
            print("utdo PQOJQWIO0EJQWIONERKOQWENKOEQW KO ")

            UserRepository.update_user(validated_data)
            
            return {"message": "Usuário atualizado com sucesso!"}, 200
        except ValidationError as e:
            return {"error": str(e)}, 400
        except (UniqueConstraintError, MissingFieldError) as e:
            return {"error": str(e)}, 400
        except ValueError as e:
            # Capturar ValueError especificamente
            return {"error": str(e)}, 400
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    def get_user(self, user_id):
        try:
            user = UserRepository.get_user(user_id)
            if user:
                user_dict = dict(zip(COLUMN_NAMES, user))
                user_dict["cpf"] = format_cpf(user_dict["cpf"])
                return {"user": user_dict}, 200
            return {"message": "Usuário não encontrado"}, 404
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    def list_users(self):
        try:
            users = UserRepository.list_users()
            if users:
                formatted_users = [
                    {**user, "cpf": format_cpf(user["cpf"])} for user in users
                ]
                return {"users": formatted_users}, 200
            return {"message": "Nenhum usuário encontrado"}, 404
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    def delete_user(self, user_id):
        try:
            if UserRepository.get_user(user_id):
                print("vou excluir")
                UserRepository.delete_user(user_id)
                return {"message": "Usuário deletado com sucesso!"}, 200
            return {"message": "Usuário não encontrado"}, 404
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)
