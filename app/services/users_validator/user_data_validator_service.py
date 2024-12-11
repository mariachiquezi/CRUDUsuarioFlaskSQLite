from datetime import datetime
from app.exceptions.validation_error import ValidationError
from app.services.users_validator.birth_validator_service import BirthDateValidator
from app.services.users_validator.cpf_validator import CPFValidator
from app.services.users_validator.email_validator_service import EmailValidatorService
from app.services.users_validator.password_validator_service import PasswordService


class UserDataValidatorService:
    @staticmethod
    def validate_data(data):
        """
        Valida os dados do usuário: email, senha, CPF e data de nascimento.
        :param email: O email do usuário.
        :param password: A senha do usuário.
        :param cpf: O CPF do usuário.
        :param birth_date: A data de nascimento do usuário (formato 'DD-MM-YYYY').
        :return: Tuple com a senha hash, CPF formatado, data de nascimento formatada e um status True se todos os dados forem válidos.
        """
        email = data["email"]
        password = data["password_hash"]
        cpf = data["cpf"]
        birth_date = data["birth_date"]

        EmailValidatorService.validate_email(email)
        print("data", birth_date)
        format_date_to_db = BirthDateValidator.validate_and_format_birth_date(
            birth_date
        )

        # Validar e criar o hash da senha
        password_hash = PasswordService.set_password(password)

        # Validar e formatar o CPF
        formatted_cpf = CPFValidator.run(cpf)

        # Se todas as validações forem bem-sucedidas, retornar os valores e True
        return password_hash, formatted_cpf, format_date_to_db, True
