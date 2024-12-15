from app.exceptions.validation_error import ValidationError
from app.repositories.user_repository import UserRepository
from app.utils.format_cpf import clean_point, format_cpf
from app.utils.format_date import get_current_timestamp
from app.services.users_validator.validation_service.validation_service import (
    prepare_user_data,
)


def extract_updated_fields(data, existing_user_dict):
    return {
        key: value
        for key, value in data.items()
        if key in existing_user_dict and existing_user_dict[key] != value
    }


def validate_and_prepare_data(data, action):

    validated_data = prepare_user_data(data, action=action)
    print('validadet_data', validated_data)
    if action == "create":
        validated_data.update(
            {
                "time_created": get_current_timestamp(),
                "time_updated": get_current_timestamp(),
            }
        )
    return validated_data


def validate_duplicate_fields(data, user_id=None):
    print("validando ")
    if "cpf" in data:
        cleaned_cpf = clean_point(data["cpf"])
        existing_user = UserRepository.check_duplicate_user(cpf=cleaned_cpf)
        if existing_user and (user_id is None or existing_user["id"] != user_id):
            raise ValidationError("CPF já está cadastrado.", status_code=409)
    print("valiodeo")
    if "email" in data:
        existing_user = UserRepository.check_duplicate_user(email=data["email"])
        if existing_user and (user_id is None or existing_user["id"] != user_id):
            raise ValidationError("Email já está cadastrado.", status_code=409)
