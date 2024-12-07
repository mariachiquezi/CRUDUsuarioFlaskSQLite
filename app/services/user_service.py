from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.user_exceptions import ValidationError
from app.repositories.user_repository import UserRepository
from app.services.cpf_validator import CPFValidator
from app.services.user_validator import ValidatorService
from db import db
from app.models.user_model import UserModel
from datetime import datetime


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, data):
        try:
            # Validar dados do usuário (email, CPF, senha e idade)
            password_hash, formatted_cpf, valid = ValidatorService.validate_user_data(
                data["email"], data["password_hash"], data["cpf"], data["age"]
            )
            if not valid:
                raise ValidationError("Dados do usuário inválidos.")

            # Criar o usuário
            user = UserModel(**data)
            user.id = ValidatorService.generate_unique_id(user.cpf)  # Gerar ID único baseado no CPF
            data["id"] = user.id
            data["password_hash"] = password_hash
            data["cpf"] = formatted_cpf
            data["time_created"] = data.get("time_created", datetime.utcnow())  # Data de criação
            data["time_updated"] = data.get("time_updated", datetime.utcnow())  # Data de atualização

            # Chamar o repositório para salvar o usuário no banco de dados
            query = self.repository.create_user()
            self.repository.save_to_db(query, data)

            return {
                "message": "Usuário criado com sucesso!"
            }, 201  # Resposta de sucesso com status 201

        except SQLAlchemyError as e:
            db.session.rollback()  # Garantir que a transação seja revertida
            error_str = str(e.__cause__)  # Obter a mensagem de erro original

            # Identificar tipo de erro específico e criar uma mensagem mais detalhada
            if "UNIQUE constraint failed" in error_str:
                if "Users.email" in error_str:
                    message = "O email já está registrado."
                elif "Users.cpf" in error_str:
                    message = "O CPF já está registrado."
                else:
                    message = "CPF ou Email já estão registrados."
                return {
                    "error": message
                }, 400  # Retornar erro com status 400 (solicitação inválida)

            # Registrar qualquer erro inesperado
            current_app.logger.error(f"Erro inesperado: {str(e)}")
            return {
                "error": "Erro desconhecido no banco de dados."
            }, 500  # Erro genérico de banco de dados

        except ValidationError as e:
            return {"error": str(e)}, 400  # Resposta de erro de validação

        except Exception as e:
            db.session.rollback()  # Reverter para garantir integridade
            current_app.logger.error(f"Erro inesperado: {str(e)}")
            return {
                "error": f"Ocorreu um erro inesperado: {str(e)}"
            }, 500  # Resposta genérica de erro

    def list_users(self):
        try:
            query = self.repository.list_users()
            result = db.session.execute(query).fetchall()
            # Converter o resultado para um dicionário
            users = [dict(row._mapping) for row in result]

            # Formatar CPF antes de retornar
            for user in users:
                user["cpf"] = CPFValidator.format_cpf(user["cpf"])

            return users, 200  # Retornar lista de usuários com status 200

        except Exception as e:
            current_app.logger.error(f"Erro ao listar usuários: {str(e)}")
            return {
                "error": str(e)
            }, 400  # Retornar resposta de erro caso a consulta ao banco falhe

    def get_user(self, id):
        try:
            query = self.repository.get_user()
            result = db.session.execute(query, {"id": id}).fetchone()
            if result:
                user = dict(result._mapping)
                # Formatar CPF antes de retornar
                user["cpf"] = CPFValidator.format_cpf(user["cpf"])
                return user, 200  # Converter Row para dict e retornar com status 200
            return {
                "error": "Usuário não encontrado"
            }, 404  # Retornar erro se o usuário não for encontrado

        except Exception as e:
            current_app.logger.error(f"Erro ao buscar usuário: {str(e)}")
            return {
                "error": str(e)
            }, 400  # Retornar resposta de erro caso a consulta ao banco falhe

    def update_user(self, id, data):
        try:
            # Validar dados do usuário (email, CPF, senha e idade)
            password_hash, formatted_cpf, valid = ValidatorService.validate_user_data(
                data["email"], data["password_hash"], data["cpf"], data["age"]
            )
            if not valid:
                raise ValidationError("Dados do usuário inválidos.")

            # Preparar os dados para atualização
            data["id"] = id
            data["password_hash"] = password_hash
            data["cpf"] = formatted_cpf
            data["time_updated"] = data.get("time_updated", datetime.utcnow())  # Atualizar timestamp

            # Chamar o repositório para atualizar o usuário no banco de dados
            query = self.repository.update_user()
            self.repository.save_to_db(query, data)

            return {
                "message": "Usuário atualizado com sucesso!"
            }, 200  # Resposta de sucesso com status 200

        except ValidationError as e:
            return {"error": str(e)}, 400  # Resposta de erro de validação

        except Exception as e:
            db.session.rollback()  # Reverter para garantir integridade
            current_app.logger.error(f"Erro ao atualizar usuário: {str(e)}")
            return {"error": str(e)}, 400  # Resposta de erro caso a atualização falhe

    def delete_user(self, id):
        try:
            # Tentar excluir o usuário
            query = self.repository.delete_user()
            result = self.repository.save_to_db(query, {"id": id})

            # Se nenhuma linha foi afetada, retornar 404 (Não encontrado)
            if not result:
                return {"error": "Usuário não encontrado"}, 404

            return {
                "message": "Usuário excluído com sucesso!"
            }, 200  # Resposta de sucesso com status 200

        except Exception as e:
            db.session.rollback()  # Reverter para garantir integridade
            current_app.logger.error(f"Erro ao excluir usuário: {str(e)}")
            return {
                "error": str(e)
            }, 400  # Retornar resposta de erro se a exclusão falhar
