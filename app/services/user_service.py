# user_service.py
from sqlite3 import IntegrityError
import sqlite3
from flask import app, jsonify
from app.repositories.user_repository import UserRepository
from app.services.validate_user_data import ValidatorService
from db import db
from app.models.user_model import UserModel
from flask import current_app


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    from flask import current_app

    def criar_usuario(self, data):
        try:
            # Criação do usuário
            user = UserModel(**data)
            user.id = ValidatorService.generate_unique_id(user.cpf)  # Gera o ID
            data["id"] = user.id

            # Valida os dados do usuário antes de fazer a inserção
            password_hash, validad = ValidatorService.validate_user_data(
                user.email, user.password_hash, user.cpf
            )
            data["password_hash"] = password_hash

            if validad:
                # Chamada para o repositório
                query = self.repository.criar_usuario()
                self.repository.save_to_db(query, data)
                return {
                    "message": "Usuário criado com sucesso!"
                }, 201  # Retorna dicionário e status

        except Exception as e:
            db.session.rollback()
            if "UNIQUE constraint failed" in str(e.orig):
                return {
                    "error": "CPF ou Email já cadastrado. Por favor, tente novamente."
                }, 400  # Retorna erro de validação de chave única

            # Usando current_app.logger para logar o erro inesperado
            current_app.logger.error(f"Erro inesperado: {str(e)}")
            return {
                "error": f"Ocorreu um erro inesperado: {str(e)}"
            }, 500  # Retorna erro genérico

    def listar_usuarios(self):
        try:
            query = self.repository.listar_usuarios()
            result = db.session.execute(query).fetchall()
            # Converte o resultado para dicionário
            usuarios = [dict(row._mapping) for row in result]
            return usuarios, 200
        except Exception as e:
            return {"error": str(e)}, 400

    def obter_usuario(self, id):
        try:
            query = self.repository.obter_usuario()
            result = db.session.execute(query, {"id": id}).fetchone()
            if result:
                return dict(result._mapping), 200  # Converte Row para dict
            return {"error": "Usuário não encontrado"}, 404
        except Exception as e:
            return {"error": str(e)}, 400

    def atualizar_usuario(self, id, data):
        try:
            query = self.repository.atualizar_usuario()
            data["id"] = id
            validad = ValidatorService.validate_user_data(
                data["email"], data["password_hash"], data["cpf"]
            )
            if validad:
                self.repository.save_to_db(query, data)
                return {"message": "Usuário atualizado com sucesso!"}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400

    def deletar_usuario(self, id):
        try:
            query = self.repository.deletar_usuario()
            self.repository.save_to_db(query, {"id": id})
            return {"message": "Usuário deletado com sucesso!"}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400
