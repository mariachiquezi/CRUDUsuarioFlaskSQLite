# data_preparation.py

from app.utils.format_cpf import clean_point
from app.utils.format_date import get_current_timestamp
from app.utils.id_generator import generate_unique_id
from app.utils.users_validator.password_validator_service import PasswordService
from app.utils.users_validators.user_data_validator_service import validate_data


def prepare_user_data(data, action):
    """Prepara os dados do usuário para criação ou atualização."""
    validated_data = validate_data(
        data, is_update=(action == "update")
    )

    user_data = {
        "name": validated_data.get("name"),
        "cpf": clean_point(validated_data.get("cpf")),
        "id": (
            generate_unique_id(validated_data.get("cpf"))
            if action == "create"
            else data.get("id")
        ),
        "email": validated_data.get("email"),
        "birth_date": validated_data.get("birth_date"),
        "password_hash": (
            PasswordService.set_password(validated_data["password_hash"])
            if validated_data.get("password_hash")
            else None
        ),
        "time_created": get_current_timestamp() if action == "create" else None,
        "time_updated": get_current_timestamp(),
    }
    return user_data


def convert_to_dict(user):
    """Converte um objeto UserModel para um dicionário."""
    user_dict = dict(user)
    user_dict.pop("_sa_instance_state", None)
    return user_dict
