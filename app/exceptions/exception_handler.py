import logging


from app.exceptions.validation_error import ValidationError


class ExceptionHandler:

    def handle_database_error(e):
        """Trata erros de banco de dados, como violação de chave única e outros erros do SQLAlchemy."""

        # Verificar se o erro é uma instância de ValidationError
        if isinstance(e, ValidationError):
            logging.error(f"Erro de validação: {str(e)}")
            return {"error": str(e)}, 400  # Retorna erro 400 para validações de dados

        # Captura o erro original de SQLAlchemy
        error_str = str(e.__cause__)

        if "UNIQUE constraint failed" in error_str:
            if "Users.email" in error_str:
                message = "O email já está registrado."
            elif "Users.cpf" in error_str:
                message = "O CPF já está registrado."
            else:
                message = "CPF ou Email já estão registrados."
            logging.error(f"Erro de violação de unicidade: {message}")
            return {"error": message}, 409  # Retorna erro 409 para conflitos de dados

        # Caso o erro não seja de unicidade
        logging.error(f"Erro inesperado no banco de dados: {str(e)}")
        return {
            "error": "Erro desconhecido no banco de dados."
        }, 500  # Erro genérico para banco de dados
        # Erro genérico de banco de dados

    def handler_validation_agr(e):
        """Trata erros de validação de dados."""
        logging.error(f"Erro de validação: {str(e)}")
        return {"error": str(e)}, 400  # Retorna erro 400 para falha de

    def handle_validation_error(e):
        """Trata erros de validação de dados."""
        logging.error(f"Erro de validação: {str(e)}")
        return {"error": str(e)}, 400  # Retorna erro 400 para falha de validação

    def handle_unique_constraint_error(e):
        """Trata violação de chave única personalizada (CPF ou Email)."""
        logging.error(f"Violação de chave única: {str(e)}")
        return {"error": str(e)}, 409  # Retorna erro 409 para conflitos de dados

    def handle_generic_error(e):
        """Trata erros inesperados."""
        logging.error(f"Erro inesperado: {str(e)}")
        return {"error": f"Ocorreu um erro inesperado: {str(e)}"}, 500  # Erro genérico

    def handle_not_found_error(e):
        """Trata erros de dados não encontrados."""
        logging.error(f"Dado não encontrado: {str(e)}")
        return {
            "error": "Recurso não encontrado."
        }, 404  # Erro 404 quando um recurso não é encontrado

    def handle_unauthorized_error(e):
        """Trata erros de autorização, como tentativas de acesso não autorizado."""
        logging.error(f"Erro de autorização: {str(e)}")
        return {
            "error": "Acesso não autorizado."
        }, 401  # Retorna erro 401 para falha de autenticação

    def handle_invalid_birthday_error(e):
        """Trata erros de formato incorreto para a data de aniversário."""
        logging.error(f"Erro de formato de data de aniversário: {str(e)}")
        return {
            "error": "Data de aniversário inválida. Use o formato AAAA-MM-DD."
        }, 400  # Erro 400 para formato inválido
