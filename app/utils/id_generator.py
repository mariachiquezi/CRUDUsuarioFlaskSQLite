import time

from app.utils.format_cpf import clean_point


def generate_unique_id(cpf):
    # Get the last 4 digits of the CPF
    last_cpf_digits = cpf[-4:]

    # Get the current timestamp in milliseconds
    timestamp = int(time.time() * 1000)  # Multiply by 1000 to get milliseconds

    # Combine the last 4 digits of CPF with the timestamp
    new_id = clean_point(f"ID{timestamp}{last_cpf_digits}")
    return new_id
