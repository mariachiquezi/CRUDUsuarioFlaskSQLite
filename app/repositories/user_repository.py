from flask import session
from app.utils.format import adjust_times_for_brasilia
from db import db
from sqlalchemy.sql import text


class UserRepository:

    @staticmethod
    def create_user(user_data):
        """
        Cria um novo usuário no banco de dados, ajustando os horários antes de salvar.
        """
        query = text(
            """
            INSERT INTO Users (id, name, birth_date, cpf, email, password_hash, time_created, time_updated)
            VALUES (:id, :name, :birth_date, :cpf, :email, :password_hash, :time_created, :time_updated)
        """
        )
        UserRepository.save_to_db(query, user_data)

    @staticmethod
    def update_user(user_data):
        """
        Atualiza os dados de um usuário no banco de dados, ajustando os horários antes de salvar.
        """
        query = text(
            """
            UPDATE Users
            SET name = :name, birth_date = :birth_date, cpf = :cpf, email = :email, password_hash = :password_hash, time_updated = :time_updated
            WHERE id = :id
        """
        )
        UserRepository.save_to_db(query, user_data)

    @staticmethod
    def get_user_by_id(user_id):
        """
        Retorna os dados de um usuário específico pelo ID.
        """
        query = text(
            """
            SELECT id, name, birth_date, cpf, email, time_created, time_updated
            FROM Users WHERE id = :id
            """
        )

        result = db.session.execute(query, {"id": user_id}).fetchone()

        return result

    @staticmethod
    def list_users():
        """
        Retorna todos os usuários.
        """
        query = text(
            """
            SELECT id, name, birth_date, cpf, email, time_created, time_updated
            FROM Users
        """
        )
        result = db.session.execute(query).fetchall()
        print("resuilt", result)
        return [dict(row._mapping) for row in result]

    @staticmethod
    def delete_user(user_id):
        """
        Deleta um usuário pelo ID.
        """
        query = text("DELETE FROM Users WHERE id = :id")
        db.session.execute(query, {"id": user_id})
        db.session.commit()

    @staticmethod
    def save_to_db(query, data):
        """
        Executa a consulta SQL e comita a transação no banco de dados, ajustando os horários antes de salvar.
        """
        try:
            data = adjust_times_for_brasilia(data)

            # Verificar se o data é um dicionário válido para ser passado
            if not isinstance(data, dict):
                raise ValueError(
                    "Os dados passados para a consulta não são um dicionário válido."
                )

            db.session.execute(query, data)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e
