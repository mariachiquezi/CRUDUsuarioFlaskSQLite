from sqlalchemy import text
from app.exceptions.error_handler import ErrorHandler
from db import db


class UserRepository:

    @staticmethod
    def create_user(user_data):
        """
        Insere um novo usuário no banco de dados.

        Parâmetros:
            user_data (dict): Dados do usuário a serem inseridos.

        Retorna:
            bool: True se o usuário for criado com sucesso, caso contrário, levanta uma exceção.
        """
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
        """
        Atualiza um usuário existente no banco de dados.

        Parâmetros:
            user_data (dict): Dados do usuário a serem atualizados.
        """
        try:
            filtered_data, set_clauses = UserRepository._formater_data(user_data)
            query = f"UPDATE Users SET {set_clauses} WHERE id = :id"
            UserRepository._execute_query(query, filtered_data)
        except Exception as e:
            ErrorHandler.handle_exception(e)

    @staticmethod
    def check_duplicate_user(cpf=None, email=None):
        """
        Verifica se um CPF ou email já está cadastrado no banco de dados.

        Parâmetros:
            cpf (string, opcional): CPF a ser verificado.
            email (string, opcional): Email a ser verificado.

        Retorna:
            dict: Dados do usuário se encontrado, caso contrário, None.
        """
        try:
            query = text(
                """
                SELECT id, cpf, email FROM Users WHERE cpf = :cpf OR email = :email LIMIT 1
            """
            )
            result = db.session.execute(query, {"cpf": cpf, "email": email}).fetchone()
            if result:
                return dict(result._mapping)
            return None
        except Exception as e:
            raise e

    @staticmethod
    def get_user(user_id):
        """
        Obtém um usuário pelo ID.

        Parâmetros:
            user_id (string): ID do usuário a ser obtido.

        Retorna:
            dict: Dados do usuário se encontrado, caso contrário, None.
        """
        try:
            query = text(
                """
                SELECT name, birth_date, cpf, email, time_created, time_updated
                FROM Users WHERE id = :id
            """
            )
            result = db.session.execute(query, {"id": user_id}).fetchone()
            if result:
                return dict(result._mapping)
            return None
        except Exception as e:
            raise e

    @staticmethod
    def get_user_to_update(user_id):
        """
        Obtém um usuário pelo ID para atualização.

        Parâmetros:
            user_id (string): ID do usuário a ser obtido.

        Retorna:
            dict: Dados do usuário se encontrado, caso contrário, None.
        """
        try:
            query = text(
                """
                SELECT name, birth_date, cpf, email, password_hash, time_updated
                FROM Users WHERE id = :id
            """
            )
            result = db.session.execute(query, {"id": user_id}).fetchone()
            if result:
                return dict(result._mapping)
            return None
        except Exception as e:
            raise e

    @staticmethod
    def list_users():
        """
        Lista todos os usuários do banco de dados.

        Retorna:
            list: Lista de dicionários contendo os dados dos usuários.
        """
        try:
            query = text(
                """
                SELECT id, name, birth_date, cpf, email, time_created, time_updated
                FROM Users
            """
            )
            result = db.session.execute(query).fetchall()
            return [dict(row._mapping) for row in result]
        except Exception as e:
            raise e

    @staticmethod
    def delete_user(user_id):
        """
        Exclui um usuário pelo ID.

        Parâmetros:
            user_id (string): ID do usuário a ser excluído.
        """
        try:
            query = "DELETE FROM Users WHERE id = :id"
            UserRepository._execute_query(query, {"id": user_id})
        except Exception as e:
            raise e

    @staticmethod
    def _execute_query(query, data):
        """
        Executa uma query no banco de dados.

        Parâmetros:
            query (string): A query SQL a ser executada.
            data (dict): Dados a serem utilizados na query.
        """
        try:
            db.session.execute(text(query), data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def _formater_data(user_data):

        filtered_data = {
            key: value for key, value in user_data.items() if value is not None
        }
        set_clauses = ", ".join(
            f"{key} = :{key}" for key in filtered_data if key != "id"
        )
        return filtered_data, set_clauses
