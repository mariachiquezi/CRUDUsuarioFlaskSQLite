class DatabaseError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UniqueConstraintError(DatabaseError):
    pass


class MissingFieldError(Exception):
    """Exceção para campos obrigatórios ausentes."""

    def __init__(self, field):
        self.field = field
        self.message = f"O campo {field} é obrigatório."
        super().__init__(self.message)
