from datetime import datetime
from app.exceptions.validation_error import ValidationError
from app.services.users_validator.birth_validator_service import AgeValidatorService
from app.services.users_validator.cpf_validator import CPFValidator
from app.services.users_validator.email_validator_service import EmailValidatorService
from app.services.users_validator.password_validator_service import PasswordService

class UserDataValidatorService:
    @staticmethod
    def validate(email, password, cpf, birth_date):
        # Validar o email
        EmailValidatorService.validate(email)

        # Validar e formatar a data de nascimento
        formatted_birth_date = AgeValidatorService.format_birth_date(birth_date)
        birth_date_obj = datetime.strptime(formatted_birth_date, "%Y-%m-%d")

        # Validar a idade (deve ser entre 18 e 110 anos)
        AgeValidatorService.validate_age(birth_date_obj)

        # Validar e criar o hash da senha
        password_hash = PasswordService.set_password(password)

        # Validar e formatar o CPF
        formatted_cpf = CPFValidator.run(cpf)

        # Se todas as validações forem bem-sucedidas, retornar valores e True
        return password_hash, formatted_cpf, formatted_birth_date, True

   
