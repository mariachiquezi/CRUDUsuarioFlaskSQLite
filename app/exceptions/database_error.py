# app/exceptions/database_error.py
class DatabaseError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UniqueConstraintError(DatabaseError):
    pass 

# app/exceptions/missing_field_error.py
class MissingFieldError(Exception):
    """Exceção para campos obrigatórios ausentes."""

    def __init__(self, field):
        self.field = field
        self.message = f"O campo {field} é obrigatório e está ausente."
        super().__init__(self.message)
