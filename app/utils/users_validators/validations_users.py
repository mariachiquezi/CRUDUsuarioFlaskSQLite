from app.constants import REQUIRED_FIELDS
from app.exceptions.database_error import MissingFieldError
from app.repositories.user_repository import UserRepository
from app.exceptions.validation_error import ValidationError
from app.models.user_model import UserModel
from app.utils.format_cpf import clean_point


def prepare_data_for_save(data, user_id=None):
    if isinstance(data, UserModel):
        data = convert_to_dict(data)
    validate_required_fields(data)
    data["id"] = None
    validate_duplicate_fields(data, user_id)
    return data


def convert_to_dict(user):
    user_dict = dict(user.__dict__)
    user_dict.pop("_sa_instance_state", None)
    return user_dict


def get_existing_user(user_id):
    existing_user = UserRepository.get_user_to_update(user_id)
    return existing_user if existing_user else None


def validate_required_fields(data):
    print("dataaaaaaaaaaaaaaaaaaa", data)
    for field in REQUIRED_FIELDS:
        if field not in data or not data[field]:
            raise MissingFieldError(field)


def validate_duplicate_fields(data, user_id=None):
    if "cpf" in data:
        cleaned_cpf = clean_point(data["cpf"])
        existing_user = UserRepository.check_duplicate_user(cpf=cleaned_cpf)
        if existing_user and (user_id is None or existing_user["id"] != user_id):
            raise ValidationError("CPF já está cadastrado.", status_code=409)
    if "email" in data:
        existing_user = UserRepository.check_duplicate_user(email=data["email"])
        if existing_user and (user_id is None or existing_user["id"] != user_id):
            raise ValidationError("Email já está cadastrado.", status_code=409)
