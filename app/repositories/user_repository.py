from app.utils.utils import CURRENT_TIMESTAMP
from db import db
from sqlalchemy.sql import text


class UserRepository:

    @staticmethod
    def create_user():
        """
        Retorna a consulta para criar um novo usuário no banco de dados.
        """
        return text(
            """
            INSERT INTO Users (id, name, age, cpf, email, password_hash, time_created, time_updated)
            VALUES (:id, :name, :age, :cpf, :email, :password_hash, :time_created, :time_updated)
            """
        )

    @staticmethod
    def list_users():
        """
        Retorna a consulta para listar todos os usuários.
        """
        return text(
            "SELECT id, name, age, cpf, email, time_created, time_updated FROM Users"
        )

    @staticmethod
    def get_user():
        """
        Retorna a consulta para buscar um usuário específico pelo id.
        """
        return text(
            "SELECT id, name, age, cpf, email, time_created, time_updated FROM Users WHERE id = :id"
        )

    @staticmethod
    def update_user():
        """
        Retorna a consulta para atualizar os dados de um usuário.
        """
        return text(
            """
            UPDATE Users
            SET name = :name, age = :age, cpf = :cpf, email = :email, password_hash = :password_hash, time_updated = :time_updated
            WHERE id = :id
            """
        )

    @staticmethod
    def delete_user():
        """
        Retorna a consulta para deletar um usuário pelo id.
        """
        return text("DELETE FROM Users WHERE id = :id")

    @staticmethod
    def save_to_db(query, data):
        """
        Executa a consulta SQL e comita a transação no banco de dados.
        """
        db.session.execute(query, data)
        db.session.commit()

    @staticmethod
    def get_current_timestamp():
        """
        Retorna o valor do timestamp atual.
        """
        return CURRENT_TIMESTAMP
