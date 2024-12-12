import pytest
from app.utils.format_cpf import clean_point, format_cpf
from app.utils.id_generator import generate_unique_id


def test_format_cpf():
    assert format_cpf("12345678901") == "123.456.789-01"


def test_clean_point_with_punctuation():
    assert clean_point("123.456-789") == "123456789"


def test_clean_point_without_punctuation():
    assert clean_point("123456789") == "123456789"


def test_clean_point_with_none():
    assert clean_point(None) is None


def test_clean_point_empty_string():
    assert clean_point("") == ""


def test_generate_unique_id():
    cpf = "12345678901"
    unique_id = generate_unique_id(cpf)
    assert unique_id.startswith("ID")
    assert unique_id.endswith(cpf[-4:])
    assert len(unique_id) > len(cpf)
