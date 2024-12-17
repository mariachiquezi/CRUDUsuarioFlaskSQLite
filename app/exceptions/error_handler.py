import logging
from flask import jsonify
from flask_limiter import RateLimitExceeded

from app.exceptions.database_error import UniqueConstraintError
from app.exceptions.validation_error import ValidationError


class ErrorHandler:
    @staticmethod
    def handle_exception(e, is_create=False):
        if is_create and "UNIQUE constraint failed" in str(e.orig):
            raise UniqueConstraintError("CPF ou Email já estão registrados.")
        raise e

    @staticmethod
    def handle_validation_error(e):
        logging.error(f"Erro de validação: {str(e)}")
        return (
            jsonify({"error": str(e)}),
            400,
        )
    
    @staticmethod
    def handle_generic_error(e):
        logging.error(f"Erro genérico: {str(e)}")
        return jsonify({"error": "Ocorreu um erro inesperado."}), 500

    @staticmethod
    def handle_not_found_error(e):
        logging.error(f"Recurso não encontrado: {str(e)}")
        return (
            jsonify({"error": "Recurso não encontrado."}),
            404,
        )

    @staticmethod
    def handle_unauthorized_error(e):
        logging.error(f"Acesso não autorizado: {str(e)}")
        return (
            jsonify({"error": "Acesso não autorizado."}),
            401,
        )


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
