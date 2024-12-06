from sqlite3 import IntegrityError

from flask import app, jsonify
from db import db
from sqlalchemy.sql import text


class UserRepository:
    @staticmethod
    def criar_usuario():
        return text(
            """
                INSERT INTO Users (id, name, age, cpf, email, password_hash, time_created, time_updated)
                VALUES (:id, :name, :age, :cpf, :email, :password_hash, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """
        )

    # Retorna dicionário e status

    @staticmethod
    def list_users():
        return text("SELECT * FROM Users")

    @staticmethod
    def get_user():
        return text("SELECT * FROM Users WHERE id = :id")

    @staticmethod
    def update_user():
        return text(
            """
            UPDATE Users
            SET name = :name, age = :age, cpf = :cpf, email = :email, password_hash = :password_hash, time_updated = CURRENT_TIMESTAMP
            WHERE id = :id
            """
        )

    @staticmethod
    def delete_user():
        return text("DELETE FROM Users WHERE id = :id")

    @staticmethod
    def save_to_db(query, data):
        """Executa a query e comita a transação no banco."""
        db.session.execute(query, data)
        db.session.commit()
