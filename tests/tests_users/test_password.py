import pytest
from app.exceptions.validation_error import ValidationError
from app.utils.users_validator.password_validator_service import PasswordService


def test_validate_password_success():
    assert PasswordService.validate_password("Password123") is True


def test_validate_password_too_short():
    with pytest.raises(ValidationError):
        PasswordService.validate_password("Pass1")


def test_validate_password_no_number():
    with pytest.raises(ValidationError):
        PasswordService.validate_password("Password")


def test_validate_password_no_letter():
    with pytest.raises(ValidationError):
        PasswordService.validate_password("12345678")


def test_set_password_success():
    password = "Password123"
    hashed_password = PasswordService.set_password(password)
    assert hashed_password.startswith(
        "$2b$12$"
    )  # Verifica se o hash é gerado pelo bcrypt


def test_check_password_success():
    password = "Password123"
    hashed_password = PasswordService.set_password(password)
    assert PasswordService.check_password(password, hashed_password) is True


def test_check_password_failure():
    password = "Password123"
    hashed_password = PasswordService.set_password(password)
    assert PasswordService.check_password("WrongPassword", hashed_password) is False
