import pytest
from app.exceptions.validation_error import ValidationError
from app.utils.users_validator.email_validator_service import EmailValidatorService


def test_validate_email_success():
    try:
        EmailValidatorService.validate_email("valid.email@example.com")
    except ValidationError:
        pytest.fail("validate_email() raised ValidationError unexpectedly!")


def test_validate_email_failure():
    with pytest.raises(ValidationError):
        EmailValidatorService.validate_email("invalid-email")
