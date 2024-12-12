from app.exceptions.validation_error import ValidationError
from app.models.user_model import UserModel
from app.services.users_validator.password_validator_service import PasswordService
from app.services.users_validator.user_data_validator_service import (
    UserDataValidatorService,
)
from app.utils.format_cpf import clean_point
from app.utils.format_date import get_current_timestamp
from app.utils.id_generator import generate_unique_id


def validate_data(data):
    """Valida os dados do usuário."""
    try:
        # Aqui instanciamos o UserModel corretamente, passando os dados
        user = UserModel(**data)
        return user.__dict__
    except Exception as e:
        raise ValidationError(f"Erro de validação: {str(e)}")


def prepare_user_data(data, action):
    print(data)
    validated_data = UserDataValidatorService.validate_data(
        data, is_update=(action == "update")
    )
    print("validated_data", validated_data)
    user_data = {
        "name": data.get("name") if data.get("name") else None,
        "cpf": (
            clean_point(validated_data.get("cpf"))
            if validated_data.get("cpf")
            else None
        ),
        "id": (
            generate_unique_id(validated_data.get("cpf"))
            if action == "create"
            else data.get("id")
        ),
        "email": validated_data.get("email") if validated_data.get("email") else None,
        "birth_date": (
            validated_data.get("birth_date")
            if validated_data.get("birth_date")
            else None
        ),
        "password_hash": (
            PasswordService.set_password(validated_data["password_hash"])
            if validated_data.get("password_hash")
            else None
        ),
        "time_created": get_current_timestamp() if action == "create" else None,
        "time_updated": get_current_timestamp(),
    }
    print("USER DATA", user_data)
    return user_data
