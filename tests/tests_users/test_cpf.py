import pytest
from app.services.users_validator.cpf_validator import CPFValidator
from app.exceptions.validation_error import ValidationError


def test_clean_cpf():
    assert CPFValidator.clean_cpf("123.456.789-09") == "12345678909"


def test_check_repetition_true():
    validator = CPFValidator("11111111111")
    assert validator.check_repetition() is True


def test_check_repetition_false():
    validator = CPFValidator("12345678909")
    assert validator.check_repetition() is False


def test_calculate_check_digit():
    validator = CPFValidator("12345678909")
    assert validator.calculate_check_digit("123456789", 10) == 0
    assert validator.calculate_check_digit("1234567890", 11) == 9


def test_validate_cpf_invalid_length():
    with pytest.raises(ValidationError):
        CPFValidator.run("1234567890")  # CPF com menos de 11 dígitos


def test_validate_cpf_sequential():
    with pytest.raises(ValidationError):
        CPFValidator.run("11111111111")  # CPF sequencial


def test_validate_cpf_valid():
    assert CPFValidator.run("123.456.789-09") == "12345678909"


def test_validate_cpf_invalid():
    with pytest.raises(ValidationError):
        CPFValidator.run("123.456.789-00")  # CPF inválido
