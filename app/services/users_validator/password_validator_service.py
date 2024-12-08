import re
from werkzeug.security import generate_password_hash, check_password_hash
from app.exceptions.validation_error import (
    ValidationError,
)  # Supondo que você tenha esta classe


class PasswordService:
    @staticmethod
    def validate_password(password):
        """Valida se a senha atende aos requisitos mínimos"""
        if (
            len(password) < 8
            or not re.search(r"[A-Za-z]", password)
            or not re.search(r"\d", password)
        ):
            raise ValidationError(
                "Senha inválida! A senha deve ter pelo menos 8 caracteres e conter uma letra e um número."
            )
        return True

    def set_password(password):
        """Gera o hash da senha e o retorna após validação"""
        if not PasswordService.validate_password(password):
            raise ValueError("A senha não atende aos requisitos de segurança.")
        return generate_password_hash(password)

    def check_password(password, password_hash):
        """Verifica se a senha fornecida corresponde ao hash armazenado"""
        return check_password_hash(password_hash, password)

    @staticmethod
    def generate_hash(password):
        """Gera o hash da senha após validá-la"""
        PasswordService.validate_password(password)
        return generate_password_hash(password)
