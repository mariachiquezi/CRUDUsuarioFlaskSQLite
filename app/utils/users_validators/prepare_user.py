from datetime import datetime
from app.exceptions.validation_error import ValidationError
from app.models.user_model import UserModel

from app.repositories.user_repository import UserRepository
from app.utils.format_cpf import clean_point
from app.utils.format_date import get_current_timestamp
from app.utils.id_generator import generate_unique_id
from app.utils.users_validator.password_validator_service import PasswordService


from app.utils.users_validators.data_preparation import prepare_user_data


def convert_to_dict(user):
    user_dict = dict(user)
    user_dict.pop("_sa_instance_state", None)
    return user_dict


def get_existing_user(user_id):
    existing_user = UserRepository.get_user_to_update(user_id)
    return existing_user if existing_user else None


def extract_updated_fields(data, existing_user_dict):
    """
    Extrai campos atualizados do dicionário de dados do usuário.

    Compara os dados fornecidos com o dicionário do usuário existente e retorna apenas os campos que foram atualizados.

    Parâmetros:
        data (dict): Dicionário contendo os dados do usuário a serem atualizados.
        existing_user_dict (dict): Dicionário do usuário existente com os dados atuais.

    Retorna:
        dict: Dicionário contendo apenas os campos que foram atualizados.
    """
    return {
        key: value
        for key, value in data.items()
        if key in existing_user_dict and existing_user_dict[key] != value
    }


def validate_and_prepare_data(data, action):
    """
    Valida e prepara os dados do usuário para criação ou atualização.

    Chama a função `prepare_user_data` para realizar a validação e preparação dos dados.
    Adiciona horario de criação e atualização se a ação for "create".

    Parâmetros:
        data (dict): Dicionário contendo os dados do usuário.
        action (str): Ação a ser realizada ("create" ou "update").

    Retorna:
        dict: Dicionário contendo os dados validados e preparados do usuário.
    """
    validated_data = prepare_user_data(data, action=action)
    print("validated_data", validated_data)
    if action == "create":
        validated_data.update(
            {
                "time_created": get_current_timestamp(),
                "time_updated": get_current_timestamp(),
            }
        )
    return validated_data
