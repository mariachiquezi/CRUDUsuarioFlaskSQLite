import logging
from flask import jsonify
from flask_limiter import RateLimitExceeded

from app.exceptions.validation_error import ValidationError
from app.exceptions.generic_error import GenericError
from app.exceptions.rate_limit_error import RateLimitError


class ErrorHandler:
    @staticmethod
    def handle_validation_error(e):
        logging.error(f"Erro de validação: {str(e)}")
        return (
            jsonify({"error": str(e)}),
            400,
        )  # Retorna erro 400 para falha de validação

    @staticmethod
    def handle_database_error(e):
        """Trata erros de banco de dados, como violação de chave única e outros erros do SQLAlchemy."""
        if isinstance(e, ValidationError):
            logging.error(f"Erro de validação: {str(e)}")
            return {"error": str(e)}, 400  # Retorna erro 400 para validações de dados

        error_str = str(e.__cause__)
        if "UNIQUE constraint failed" in error_str:
            print("WERORRORRR", error_str)
            if "Users.email" in error_str:
                message = "O email já está registrado."
            elif "Users.cpf" in error_str:
                message = "O CPF já está registrado."
            else:
                message = "CPF ou Email já estão registrados."
            print("vou madnar")
            return {"error": message}, 409  # Retorna erro 409 para conflitos de dados
        elif "NOT NULL constraint failed" in error_str:
            if "Users.password_hash" in error_str:
                message = "A senha é obrigatória."
            else:
                message = "Campo obrigatório não preenchido."
            logging.error(f"Erro de campo obrigatório: {message}")
            return {
                "error": message
            }, 400  # Retorna erro 400 para falha de campo obrigatório
        logging.error(f"Erro inesperado no banco de dados: {str(e)}")
        return {
            "error": "Erro desconhecido no banco de dados."
        }, 500  # Erro genérico para banco de dados

    @staticmethod
    def handle_rate_limit_error(e):
        logging.error(f"Limite de requisições excedido: {str(e)}")
        return (
            jsonify({"error": str(e)}),
            429,
        )  # Retorna erro 429 para excesso de requisições

    @staticmethod
    def handle_generic_error(e):
        logging.error(f"Erro genérico: {str(e)}")
        return jsonify({"error": "Ocorreu um erro inesperado."}), 500  # Erro genérico

    @staticmethod
    def handle_not_found_error(e):
        logging.error(f"Recurso não encontrado: {str(e)}")
        return (
            jsonify({"error": "Recurso não encontrado."}),
            404,
        )  # Erro 404 quando o recurso não é encontrado

    @staticmethod
    def handle_unauthorized_error(e):
        logging.error(f"Acesso não autorizado: {str(e)}")
        return (
            jsonify({"error": "Acesso não autorizado."}),
            401,
        )  # Erro 401 quando não autorizado

    @staticmethod
    def handle_unique_constraint_error(e):
        logging.error(f"Erro de violação de unicidade: {str(e)}")
        return (
            jsonify({"error": str(e)}),
            409,
        )  # Retorna erro 409 para conflitos de dados


def register_error_handlers(app):
    """Registra os manipuladores de erro no app Flask."""

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return ErrorHandler.handle_validation_error(e)

  

    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit_error(e):
        return ErrorHandler.handle_rate_limit_error(e)


    @app.errorhandler(Exception)
    def handle_generic_error(e):
        return ErrorHandler.handle_generic_error(e)

    @app.errorhandler(404)
    def handle_not_found_error(e):
        return ErrorHandler.handle_not_found_error(e)

    @app.errorhandler(401)
    def handle_unauthorized_error(e):
        return ErrorHandler.handle_unauthorized_error(e)
