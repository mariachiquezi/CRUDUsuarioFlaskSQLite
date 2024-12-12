def format_cpf(cpf):
    formatted_cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    return formatted_cpf


def clean_point(value):
    return value.replace(".", "").replace("-", "")
