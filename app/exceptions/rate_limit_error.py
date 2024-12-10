# app/exceptions/rate_limit_error.py
class RateLimitError(Exception):
    def __init__(self, message="Limite de requisições excedido. Tente novamente mais tarde."):
        self.message = message
        super().__init__(self.message)
