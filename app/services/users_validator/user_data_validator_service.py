from app.exceptions.validation_error import ValidationError
from app.services.users_validator.birth_validator_service import BirthDateValidator
from app.services.users_validator.cpf_validator import CPFValidator
from app.services.users_validator.email_validator_service import EmailValidatorService
from app.services.users_validator.password_validator_service import PasswordService


class UserDataValidatorService:
    
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
    def validate_birth_date(birth_date):
        print("data",birth_date)
        if not birth_date:
            raise ValidationError("Data de nascimento é obrigatória.")
        return BirthDateValidator.validate_and_format_birth_date(birth_date)

    @staticmethod
    def validate_password(password):
        return PasswordService.set_password(password) if password else None

    @staticmethod
    def validate_data(data, is_update=False):
        validated_data = {}
        print("datra111111", data)
        if "email" in data:
            validated_data["email"] = UserDataValidatorService.validate_email(
                data["email"]
            )
        print("email valido")
        if "cpf" in data or not is_update:
            validated_data["cpf"] = UserDataValidatorService.validate_cpf(
                data.get("cpf")
            )
        print("cpf valido")
        if "birth_date" in data or not is_update:
            validated_data["birth_date"] = UserDataValidatorService.validate_birth_date(
                data.get("birth_date")
            )
        print("birth_date valido")
        if "password_hash" in data:
            validated_data["password_hash"] = (
                UserDataValidatorService.validate_password(data["password_hash"])
            )
        print("password_hash valido")
        validated_data["name"] = data.get("name")  
        print("validadosim", validated_data)
        return validated_data
