from app.exceptions.validation_error import ValidationError
from validators.email import email as validate_email

class EmailValidatorService:
    @staticmethod
    def validate(email):
        if not validate_email(email):
            raise ValidationError(
                "Email inválido! Por favor, verifique e tente novamente"
            )
