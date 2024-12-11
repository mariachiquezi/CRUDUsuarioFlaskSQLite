from app.exceptions.validation_error import ValidationError
from app.models.user_model import UserModel
from app.services.users_validator.user_data_validator_service import (
    UserDataValidatorService,
)
from app.utils.format import get_current_timestamp
from app.utils.id_generator import generate_unique_id


def validate_data(data):
    """Valida os dados do usuário."""
    try:
        # Aqui instanciamos o UserModel corretamente, passando os dados
        user = UserModel(**data)
        return user.__dict__
    except Exception as e:
        raise ValidationError(f"Erro de validação: {str(e)}")


def prepare_user_data(validated_data, user_id=None):
    """
    Prepara os dados do usuário para criação ou atualização.
    """
    password_hash, formatted_cpf, formatted_birth_date, valid = (
        UserDataValidatorService.validate_data(validated_data)
    )
    if not valid:
        raise ValidationError("Dados do usuário inválidos.")

    # Prepare o dicionário de dados do usuário
    user_data = {
        "password_hash": password_hash,
        "name": validated_data.get("name"),  # Acessando o atributo diretamente
        "cpf": formatted_cpf,
        "email": validated_data.get("email"),
        "birth_date": formatted_birth_date,
        "id": user_id or generate_unique_id(formatted_cpf),
        "time_created": get_current_timestamp(),  # Ajuste do timestamp
        "time_updated": get_current_timestamp(),
    }

    return user_data
