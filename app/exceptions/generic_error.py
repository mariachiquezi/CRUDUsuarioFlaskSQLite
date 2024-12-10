# app/exceptions/generic_error.py
class GenericError(Exception):
    def __init__(self, message="Ocorreu um erro inesperado."):
        self.message = message
        super().__init__(self.message)
