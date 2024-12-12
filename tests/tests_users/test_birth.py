import pytest
from datetime import datetime

from app.services.users_validator.birth_validator_service import BirthDateValidator


def test_normalize_date_format():
    assert BirthDateValidator.normalize_date_format("01/01/2000") == "01-01-2000"


def test_parse_birth_date():
    birth_date = "01-01-2000"
    parsed_date = BirthDateValidator.parse_birth_date(birth_date)
    assert parsed_date == datetime.strptime(birth_date, "%d-%m-%Y")


def test_parse_birth_date_invalid_format():
    with pytest.raises(ValueError):
        BirthDateValidator.parse_birth_date("2000-01-01")  # Formato inválido


def test_validate_age_within_range():
    birth_date = "01-01-2000"
    birth_date_obj = BirthDateValidator.parse_birth_date(birth_date)
    BirthDateValidator.validate_age(birth_date_obj)  # Não deve levantar exceção


def test_validate_age_below_minimum():
    birth_date = (
        datetime.today().replace(year=datetime.today().year - 10).strftime("%d-%m-%Y")
    )
    birth_date_obj = BirthDateValidator.parse_birth_date(birth_date)
    with pytest.raises(ValueError):
        BirthDateValidator.validate_age(birth_date_obj)  # Idade abaixo do mínimo


def test_validate_age_above_maximum():
    birth_date = (
        datetime.today().replace(year=datetime.today().year - 120).strftime("%d-%m-%Y")
    )
    birth_date_obj = BirthDateValidator.parse_birth_date(birth_date)
    with pytest.raises(ValueError):
        BirthDateValidator.validate_age(birth_date_obj)  # Idade acima do máximo


def test_format_date_to_db():
    birth_date = "01-01-2000"
    birth_date_obj = BirthDateValidator.parse_birth_date(birth_date)
    assert BirthDateValidator.format_date_to_db(birth_date_obj) == "2000-01-01"


def test_calculate_age():
    birth_date = "01-01-2000"
    birth_date_obj = BirthDateValidator.parse_birth_date(birth_date)
    calculated_age = BirthDateValidator.calculate_age(birth_date_obj)
    expected_age = (
        datetime.today().year
        - 2000
        - ((datetime.today().month, datetime.today().day) < (1, 1))
    )
    assert calculated_age == expected_age


def test_validate_and_format_birth_date():
    birth_date = "01-01-2000"
    formatted_date = BirthDateValidator.validate_and_format_birth_date(birth_date)
    assert formatted_date == "2000-01-01"


def test_validate_and_format_birth_date_invalid_format():
    with pytest.raises(ValueError):
        BirthDateValidator.validate_and_format_birth_date(
            "2000-01-01"
        )  # Formato inválido