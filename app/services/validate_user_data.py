import re
import time
from app.exceptions.user_exceptions import ValidationError
from app.services.validate_cpf import CPFValidator
from werkzeug.security import generate_password_hash, check_password_hash
from validators.email import email as validate_email


class ValidatorService:
    @staticmethod
    def validate_email(email):
        if not validate_email(email):
            raise ValidationError(
                "Email inválido! Por favor, verifique e tente novamente"
            )

    @staticmethod
    def validate_password(password):
        print("password", password)
        if (
            len(password) < 8
            or not re.search(r"[A-Za-z]", password)
            or not re.search(r"\d", password)
        ):
            raise ValidationError(
                "Senha inválida! A senha deve ter pelo menos 8 caracteres e conter uma letra maiúscula, uma minúscula e um número."
            )
        print("PQ NAO ASPS")
        return True

    @staticmethod
    def generate_unique_id(cpf):
        # Get the last 4 digits of the CPF
        last_cpf_digits = cpf[-4:]

        # Get the current timestamp in milliseconds
        timestamp = int(time.time() * 1000)  # Multiply by 1000 to get milliseconds

        # Combine the last 4 digits of CPF with the timestamp
        new_id = f"ID{timestamp}{last_cpf_digits}"

        return new_id

    def set_password(self, password):
        """Generates the password hash and stores it in the database after validating the password."""
        if not self.validate_password(password):
            raise ValueError("A senha não atende aos requisitos de segurança.")
        return generate_password_hash(password)
        print("passssss", self.password_hash)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def validate_user_data(email, password, cpf):
        # Validates a user's data in a single function
        ValidatorService.validate_email(email)
        password_hash = ValidatorService().set_password(password)
        CPFValidator.run(cpf)
        return password_hash, True
