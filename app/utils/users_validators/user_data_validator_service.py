from app.exceptions.validation_error import ValidationError
from app.utils.users_validator.birth_validator_service import BirthDateValidator
from app.utils.users_validator.cpf_validator import CPFValidator
from app.utils.users_validator.email_validator_service import EmailValidatorService
from app.utils.users_validator.password_validator_service import PasswordService


@staticmethod
def validate_email(email):
    EmailValidatorService.validate_email(email)
    return email


@staticmethod
def validate_cpf(cpf):
    if not cpf:
        raise ValidationError("CPF é obrigatório.")
    return CPFValidator.run(cpf)


@staticmethod
def validate_password(password):
    return PasswordService.set_password(password) if password else None


@staticmethod
def validate_data(data, is_update=False):
    validated_data = {}
    if "email" in data:
        validated_data["email"] = validate_email(data["email"])
    if "cpf" in data:
        validated_data["cpf"] = validate_cpf(data.get("cpf"))
    elif not is_update:  # Se não é uma atualização e CPF não está nos dados
        raise ValidationError("CPF é obrigatório para novas criações.")
    if "birth_date" in data or not is_update:
        validated_data["birth_date"] = (
            BirthDateValidator.validate_and_format_birth_date(data.get("birth_date"))
        )
    if "password_hash" in data:
        validated_data["password_hash"] = validate_password(data["password_hash"])
    validated_data["name"] = data.get("name")
    return validated_data
