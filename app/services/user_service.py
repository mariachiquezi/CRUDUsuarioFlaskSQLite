# app/services/user_service.py
from app.exceptions.database_error import UniqueConstraintError
from app.exceptions.validation_error import ValidationError
from app.repositories.user_repository import UserRepository
from app.services.users_validator.user_data_validator_service import (
    UserDataValidatorService,
)
from app.utils.id_generator import generate_unique_id
from app.utils.format import format_cpf, get_current_timestamp
from app.models.user_model import UserModel  # Modelo do usuário no SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.error_handler import ErrorHandler


class UserService:
    def __init__(self):
        self.generate_unique_id = generate_unique_id
        self.validator = UserDataValidatorService()

    def create_user(self, data):
        """Cria um novo usuário com base nos dados recebidos."""
        return self._save_user(data, "create")

    def update_user(self, user_id, data):
        """Atualiza um usuário existente com base no ID e dados fornecidos."""
        data["id"] = user_id  # Passa o user_id para o update
        return self._save_user(data, "update")

    def get_user_by_id(self, user_id):
        """Obtém os dados de um usuário pelo ID."""
        try:
            user = UserRepository.get_user_by_id(user_id)
            if user:
                # Converte o objeto do modelo UserModel para dicionário usando to_dict()
                return {"user": user.to_dict()}, 200
            return {"message": "Usuário não encontrado"}, 404
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    def list_users(self):
        """Lista os dados de todos os usuários."""
        try:
            users = UserRepository.list_users()
            if users:
                # Converte a lista de objetos do modelo UserModel para dicionários
                return {"users": [user.to_dict() for user in users]}, 200
            return {"message": "Nenhum usuário encontrado"}, 404
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    def delete_user(self, user_id):
        """Deleta um usuário pelo ID."""
        try:
            user = UserRepository.get_user_by_id(user_id)
            if user:
                UserRepository.delete_user(user_id)
                return {"message": "Usuário excluído com sucesso!"}, 200
            return {"message": "Usuário não encontrado"}, 404
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    def _save_user(self, data, action):
        """
        Função genérica para salvar ou atualizar um usuário.

        :param data: Dados do usuário.
        :param action: Ação que será realizada - 'create' ou 'update'.
        """
        try:
            # Valida e prepara os dados
            validated_data = self._validate_data(data)
            print("valdiaaaaaaaa", validated_data)
            user_data = self._prepare_user_data(validated_data, data.get("id"))
            print("user_data", user_data)
            # Salva ou atualiza no banco de dados
            if action == "create":
                UserRepository.create_user(user_data)
                return {"message": "Usuário criado com sucesso!"}, 201
            elif action == "update":
                UserRepository.update_user(user_data)
                return {"message": "Usuário atualizado com sucesso!"}, 200

        except (UniqueConstraintError, SQLAlchemyError) as e:
            return ErrorHandler.handle_database_error(e)
        except ValidationError as e:  # Captura erros de validação
            return {"error": str(e)}, 400
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    def _validate_data(self, data):
        """Valida os dados do usuário."""
        try:
            # Aqui instanciamos o UserModel corretamente, passando os dados
            user = UserModel(**data)  
            print("usserrrrrr", user.__dict__)
            return user.__dict__
        except Exception as e:
            raise ValidationError(f"Erro de validação: {str(e)}")

    def _prepare_user_data(self, validated_data, user_id=None):
        """
        Prepara os dados do usuário para criação ou atualização.
        """
        print("validadedata", validated_data)
        password_hash, formatted_cpf, formatted_birth_date, valid = (
            self.validator.validate_data(validated_data)
        )
        if not valid:
            raise ValidationError("Dados do usuário inválidos.")

        # Prepare o dicionário de dados do usuário
        user_data = {
            "password_hash": password_hash,
            "name": validated_data.get("name"),  # Acessando o atributo diretamente
            "cpf": formatted_cpf,
            "email": validated_data.get("email"),
            "birth_date": formatted_birth_date,
            "id": user_id or self.generate_unique_id(validated_data.cpf),
            "time_created": get_current_timestamp(),  # Ajuste do timestamp
            "time_updated": get_current_timestamp(),
        }

        return user_data
