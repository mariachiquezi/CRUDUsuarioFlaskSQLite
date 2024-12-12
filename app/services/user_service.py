import traceback
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
from app.utils.format_cpf import clean_point, format_cpf
from app.utils.format_date import get_current_timestamp
from app.utils.id_generator import generate_unique_id
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.error_handler import ErrorHandler


class UserService:
    def create_user(self, data):
        try:
            data["id"] = None
            valid = validate_data(data)
            validated_data = prepare_user_data(valid, action="create")
            validated_data.update(
                {
                    "time_created": get_current_timestamp(),
                    "time_updated": get_current_timestamp(),
                }
            )
            valid_unique = self._validate_duplicate_fields(validated_data)
            UserRepository.create_user(validated_data)
            return {"message": "Usuário criado com sucesso!"}, 201
        except (UniqueConstraintError, ValidationError) as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    def update_user(self, user_id, data):
        try:
            existing_user = UserRepository.get_user(user_id)
            if not existing_user:
                return {"message": "Usuário não encontrado"}, 404

            updated_fields = self._extract_updated_fields(
                data, dict(zip(COLUMN_NAMES, existing_user))
            )
            if not updated_fields:
                return {"message": "Nenhuma alteração detectada."}, 400

            self._validate_duplicate_fields(updated_fields, user_id)
            validated_data = prepare_user_data(updated_fields, action="update")
            validated_data["id"] = user_id
            validated_data["time_updated"] = get_current_timestamp()

            UserRepository.update_user(validated_data)
            return {"message": "Usuário atualizado com sucesso!"}, 200

        except ValidationError as e:
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
                UserRepository.delete_user(user_id)
                return {"message": "Usuário excluído com sucesso!"}, 200
            return {"message": "Usuário não encontrado"}, 404
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    def _extract_updated_fields(self, data, existing_user_dict):
        return {
            key: value
            for key, value in data.items()
            if key in existing_user_dict and existing_user_dict[key] != value
        }

    def _validate_duplicate_fields(self, user_id, updated_fields):
        if "cpf" in updated_fields:
            cleaned_cpf = clean_point(updated_fields["cpf"])
            existing_user = UserRepository.check_duplicate_user(cpf=cleaned_cpf)
            if existing_user and existing_user["id"] != user_id:
                raise ValidationError("CPF já está cadastrado.")

        if "email" in updated_fields:
            existing_user = UserRepository.check_duplicate_user(
                email=updated_fields["email"]
            )
            if existing_user and existing_user["id"] != user_id:
                raise ValidationError("Email já está cadastrado.")
