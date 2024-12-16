import time

from app.utils.format_cpf import clean_point


def generate_unique_id(cpf):
    last_cpf_digits = cpf[-4:]

    timestamp = int(time.time() * 1000)

    new_id = clean_point(f"ID{timestamp}{last_cpf_digits}")
    return new_id
