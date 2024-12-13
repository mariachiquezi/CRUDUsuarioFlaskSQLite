from sqlalchemy import text
from app.exceptions.database_error import UniqueConstraintError
from app.exceptions.error_handler import ErrorHandler
from db import db

class UserRepository:
    
    @staticmethod
    def create_user(user_data):
        try:
            query = """
                INSERT INTO Users (id, name, birth_date, cpf, email, password_hash, time_created, time_updated)
                VALUES (:id, :name, :birth_date, :cpf, :email, :password_hash, :time_created, :time_updated)
            """
            UserRepository._execute_query(query, user_data)
            return True
        except Exception as e:
            ErrorHandler.handle_exception(e, is_create=True)

    @staticmethod
    def update_user(user_data):
        try:
            filtered_data = {key: value for key, value in user_data.items() if value is not None}
            set_clauses = ", ".join(f"{key} = :{key}" for key in filtered_data if key != "id")
            query = f"UPDATE Users SET {set_clauses} WHERE id = :id"
            UserRepository._execute_query(query, filtered_data)
        except Exception as e:
            ErrorHandler.handle_exception(e)

    @staticmethod
    def check_duplicate_user(cpf=None, email=None):
        try:
            query = text("""
                SELECT id, cpf, email FROM Users WHERE cpf = :cpf OR email = :email LIMIT 1
            """)
            result = db.session.execute(query, {"cpf": cpf, "email": email}).fetchone()
            if result:
                return dict(result._mapping)
            return None
        except Exception as e:
            raise e

    @staticmethod
    def get_user(user_id):
        try:
            query = text("""
                SELECT name, birth_date, cpf, email, time_created, time_updated
                FROM Users WHERE id = :id
            """)
            result = db.session.execute(query, {"id": user_id}).fetchone()
            if result:
                return dict(result._mapping)
            return None
        except Exception as e:
            raise e
    @staticmethod
    def get_user_to_update(user_id):
        try:
            query = text("""
                SELECT name, birth_date, cpf, email, password_hash, time_updated
                FROM Users WHERE id = :id
            """)
            result = db.session.execute(query, {"id": user_id}).fetchone()
            if result:
                print("REUSLTIRRRRRR", result)
                return dict(result._mapping)
            return None
        except Exception as e:
            raise e
    @staticmethod
    def list_users():
        try:
            query = text("""
                SELECT id, name, birth_date, cpf, email, time_created, time_updated
                FROM Users
            """)
            result = db.session.execute(query).fetchall()
            return [dict(row._mapping) for row in result]
        except Exception as e:
            raise e

    @staticmethod
    def delete_user(user_id):
        try:
            query = "DELETE FROM Users WHERE id = :id"
            UserRepository._execute_query(query, {"id": user_id})
        except Exception as e:
            raise e

    @staticmethod
    def _execute_query(query, data):
        try:
            db.session.execute(text(query), data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e  # Levanta a exceção para ser tratada na camada de serviço

   