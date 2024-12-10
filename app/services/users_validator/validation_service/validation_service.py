from app.services.users_validator.user_data_validator_service import (
    UserDataValidatorService,
)


def return_data(data):
    # Chama a validação de idade antes de continuar com os outros dados
    valids = UserDataValidatorService.validate_data(
        data["email"], data["password_hash"], data["cpf"], data["birth_date"]
    )

    return valids


