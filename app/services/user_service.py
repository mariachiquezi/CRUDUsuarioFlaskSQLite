from app.constants import COLUMN_NAMES, REQUIRED_FIELDS
from app.exceptions.database_error import MissingFieldError, UniqueConstraintError
from app.exceptions.validation_error import ValidationError
from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository
from app.utils.validations_users import (
    extract_updated_fields,
    validate_and_prepare_data,
    validate_duplicate_fields,
)
from app.utils.format_cpf import format_cpf
from app.exceptions.error_handler import ErrorHandler
from app.utils.format_date import get_current_timestamp


class UserService:
    def create_user(self, data):
        try:
            print("data",data)
            if isinstance(data, UserModel): 
                data = dict(data.__dict__) 
                data.pop('_sa_instance_state', None)
            self._validate_required_fields(data)
            print("valido")
            data["id"] = None  # Garantir que o id não seja fornecido
            validate_duplicate_fields(data)
            validated_data = validate_and_prepare_data(data, "create")
            user = UserRepository.create_user(validated_data)
            return {"message": "Usuário criado com sucesso!"}, 201
        except (
            ValidationError,
            UniqueConstraintError,
            MissingFieldError,
            ValueError,
        ) as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    def update_user(self, user_id, data):
        try:
            if isinstance(data, UserModel): 
                data = dict(data.__dict__) 
                data.pop('_sa_instance_state', None)
            existing_user = self._get_existing_user(user_id)
            if not existing_user:
                return {"message": "Usuário não encontrado"}, 404

            updated_fields = extract_updated_fields(
                data, dict(zip(COLUMN_NAMES, existing_user))
            )
            if not updated_fields:
                return {"message": "Nenhuma alteração detectada."}, 400

            validate_duplicate_fields(updated_fields, user_id)
            validated_data = validate_and_prepare_data(updated_fields, "update")
            validated_data["id"] = user_id
            validated_data["time_updated"] = get_current_timestamp()

            UserRepository.update_user(validated_data)
            return {"message": "Usuário atualizado com sucesso!"}, 200
        except (
            ValidationError,
            UniqueConstraintError,
            MissingFieldError,
            ValueError,
        ) as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    def get_user(self, user_id):
        try:
            user = UserRepository.get_user(user_id)
            if user:
                user_dict = dict(user)
                user_dict.pop("_sa_instance_state", None)
                user_dict["cpf"] = format_cpf(user_dict["cpf"])

                print("user_dict", user_dict)
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
                for user in formatted_users:
                    user.pop("_sa_instance_state", None)
                return {"users": formatted_users}, 200
            return {"message": "Nenhum usuário encontrado"}, 404
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    def delete_user(self, user_id):
        try:
            if UserRepository.get_user(user_id):
                UserRepository.delete_user(user_id)
                return {"message": "Usuário deletado com sucesso!"}, 200
            return {"message": "Usuário não encontrado"}, 404
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    def _get_existing_user(self, user_id):
        existing_user = UserRepository.get_user_to_update(user_id)
        if not existing_user:
            return None
        return existing_user

    def _validate_required_fields(self, data): 
        print("Validando campos obrigatórios para os dados:", data)
        for field in REQUIRED_FIELDS: 
            if field not in data: 
                print(f"Campo obrigatório ausente: {field}") 
                raise MissingFieldError(field) 
            if not data[field]: 
                print(f"Campo obrigatório vazio: {field}") 
                raise MissingFieldError(field) 
    print("Todos os campos obrigatórios estão presentes e preenchidos.")
