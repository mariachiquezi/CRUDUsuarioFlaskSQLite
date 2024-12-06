class ValidationError(Exception):
    """Exceção personalizada para erros de validação de dados."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
