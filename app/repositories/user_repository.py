from sqlalchemy import text
from db import db


class UserRepository:
    @staticmethod
    def create_user(user_data):
        UserRepository._execute_query(
            """
            INSERT INTO Users (id, name, birth_date, cpf, email, password_hash, time_created, time_updated)
            VALUES (:id, :name, :birth_date, :cpf, :email, :password_hash, :time_created, :time_updated)
            """,
            user_data,
        )

    @staticmethod
    def update_user(user_data):
        # Filtrar valores None
        filtered_data = {key: value for key, value in user_data.items() if value is not None}
        set_clauses = ", ".join(f"{key} = :{key}" for key in filtered_data if key != "id")
        query = f"UPDATE Users SET {set_clauses} WHERE id = :id"
        UserRepository._execute_query(query, filtered_data)


    @staticmethod
    def check_duplicate_user(cpf=None, email=None):
        query = text(
            """
        SELECT 1 FROM Users WHERE cpf = :cpf OR email = :email LIMIT 1
        """
        )
        result = db.session.execute(query, {"cpf": cpf, "email": email}).fetchone()
        return result is not None

    @staticmethod
    def get_user(user_id):
        query = text(
            """
        SELECT id, name, birth_date, cpf, email, time_created, time_updated
        FROM Users WHERE id = :id
        """
        )
        return db.session.execute(query, {"id": user_id}).fetchone()

    @staticmethod
    def list_users():
        query = text(
            """
        SELECT id, name, birth_date, cpf, email, time_created, time_updated
        FROM Users
        """
        )
        return [dict(row._mapping) for row in db.session.execute(query).fetchall()]

    @staticmethod
    def delete_user(user_id):
        UserRepository._execute_query(
            "DELETE FROM Users WHERE id = :id", {"id": user_id}
        )

    @staticmethod
    def _execute_query(query, data):
        try:
            db.session.execute(text(query), data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
