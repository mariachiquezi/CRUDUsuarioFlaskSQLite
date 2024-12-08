from app.services.users_validator.birth_validator_service import BirthFormatter
from app.services.users_validator.email_validator_service import EmailValidatorService
from app.services.users_validator.password_validator_service import PasswordService
from app.services.users_validator.cpf_validator import CPFValidator


class UserDataValidatorService:
    @staticmethod
    def validate(email, password, cpf, birth_date):
        # Validar o email
        EmailValidatorService.validate(email)
        # Validar a idade
        formatted_birth_date = BirthFormatter.format_birth_date(birth_date)
        # Validar e criar o hash da senha
        password_hash = PasswordService.set_password(password)
        # Validar e formatar o CPF
        formatted_cpf = CPFValidator.run(cpf)

        # Se todas as validações forem bem-sucedidas, retornar valores e True
        return password_hash, formatted_cpf, formatted_birth_date, True
