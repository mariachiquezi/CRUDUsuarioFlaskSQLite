from http.client import HTTPResponse
from sqlite3 import IntegrityError


class ValidationError(Exception):
    """Exceção personalizada para erros de validação de dados."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
class UniqueConstraintViolationError(Exception):
    def __init__(self, message="Violação de chave única (CPF ou Email já cadastrados)."):
        self.message = message
        super().__init__(self.message)
