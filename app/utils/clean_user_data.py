from app.utils.format_cpf import clean_point


def clean_user_data(data):
    """Remove pontuação do CPF e ID dos dados do usuário."""
    if "id" in data:
        del data["id"]
    if "cpf" in data:
        data["cpf"] = clean_point(data["cpf"])
    return data
