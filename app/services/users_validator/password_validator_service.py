import re
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from app.exceptions.validation_error import (
    ValidationError,
)  # Supondo que você tenha esta classe


class PasswordService:
    def validate_password(password):
        print("password", password)
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
        generate_hash = PasswordService.generate_hash(password)
        return generate_hash

    def check_password(password, password_hash):
        """Verifica se a senha fornecida corresponde ao hash armazenado"""
        return check_password_hash(password_hash, password)

    def generate_hash(password):
        """
        Gera um hash para a senha usando bcrypt com fator de custo 12.
        """
        password_bytes = password.encode("utf-8")  # Convertendo a senha para bytes
        salt = bcrypt.gensalt(rounds=12)
        hashed_password = bcrypt.hashpw(password_bytes, salt).decode("utf-8")
        return hashed_password
