# app/exceptions/database_error.py
class DatabaseError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class UniqueConstraintError(DatabaseError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
