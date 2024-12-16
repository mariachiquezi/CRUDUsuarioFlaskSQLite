import re
import bcrypt
from app.exceptions.validation_error import ValidationError


class PasswordService:
    @staticmethod
    def validate_password(password):
        """Valida se a senha atende aos requisitos"""
        if (
            len(password) < 8
            or not re.search(r"[A-Za-z]", password)
            or not re.search(r"\d", password)
        ):
            raise ValidationError(
                "Senha inválida! A senha deve ter pelo menos 8 caracteres e conter uma letra e um número."
            )
        return True

    @staticmethod
    def set_password(password):
        """Gera o hash da senha"""
        if not PasswordService.validate_password(password):
            raise ValueError("A senha não atende aos requisitos de segurança.")
        return PasswordService.generate_hash(password)

    @staticmethod
    def check_password(password, password_hash):
        """Verifica se a senha corresponde ao hash armazenado"""
        password_bytes = password.encode("utf-8")
        return bcrypt.checkpw(password_bytes, password_hash.encode("utf-8"))

    @staticmethod
    def generate_hash(password):
        """
        Gera um hash para a senha usando bcrypt
        """
        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt(rounds=12)
        hashed_password = bcrypt.hashpw(password_bytes, salt).decode("utf-8")
        return hashed_password
