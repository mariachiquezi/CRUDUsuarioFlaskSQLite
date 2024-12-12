def format_cpf(cpf):
    formatted_cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    return formatted_cpf


def clean_point(value):
    # Verifica se o valor contém pontuação antes de substituir
    if value and ('.' in value or '-' in value):
        return value.replace(".", "").replace("-", "")
    return value

