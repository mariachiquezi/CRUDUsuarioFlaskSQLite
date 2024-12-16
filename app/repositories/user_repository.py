import logging
from sqlalchemy import text
from app.exceptions.error_handler import ErrorHandler
from db import db

# Configuração básica do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
            logger.info("Iniciando criação de usuário.")
            query = """
                INSERT INTO Users (id, name, birth_date, cpf, email, password_hash, time_created, time_updated)
                VALUES (:id, :name, :birth_date, :cpf, :email, :password_hash, :time_created, :time_updated)
            """
            UserRepository._execute_query(query, user_data)
            logger.info("Usuário criado com sucesso.")
            return True
        except Exception as e:
            logger.error(f"Erro ao criar usuário: {str(e)}")
            ErrorHandler.handle_exception(e, is_create=True)

    @staticmethod
    def update_user(user_data):
        """
        Atualiza um usuário existente no banco de dados.

        Parâmetros:
            user_data (dict): Dados do usuário a serem atualizados.
        """
        try:
            logger.info(f"Iniciando atualização do usuário com ID: {user_data['id']}")
            filtered_data, set_clauses = UserRepository._formater_data(user_data)
            query = f"UPDATE Users SET {set_clauses} WHERE id = :id"
            UserRepository._execute_query(query, filtered_data)
            logger.info(f"Usuário com ID {user_data['id']} atualizado com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao atualizar usuário: {str(e)}")
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
            logger.info("Verificando duplicidade de CPF ou email.")
            query = text(
                """
                SELECT id, cpf, email FROM Users WHERE cpf = :cpf OR email = :email LIMIT 1
            """
            )
            result = db.session.execute(query, {"cpf": cpf, "email": email}).fetchone()
            if result:
                logger.info("Duplicidade encontrada.")
                return dict(result._mapping)
            logger.info("Nenhuma duplicidade encontrada.")
            return None
        except Exception as e:
            logger.error(f"Erro ao verificar duplicidade: {str(e)}")
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
            logger.info(f"Buscando usuário com ID: {user_id}")
            query = text(
                """
                SELECT name, birth_date, cpf, email, time_created, time_updated
                FROM Users WHERE id = :id
            """
            )
            result = db.session.execute(query, {"id": user_id}).fetchone()
            if result:
                logger.info(f"Usuário com ID {user_id} encontrado.")
                return dict(result._mapping)
            logger.info(f"Usuário com ID {user_id} não encontrado.")
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar usuário: {str(e)}")
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
            logger.info(f"Buscando usuário com ID {user_id} para atualização.")
            query = text(
                """
                SELECT name, birth_date, cpf, email, password_hash, time_updated
                FROM Users WHERE id = :id
            """
            )
            result = db.session.execute(query, {"id": user_id}).fetchone()
            if result:
                logger.info(f"Usuário com ID {user_id} encontrado para atualização.")
                return dict(result._mapping)
            logger.info(f"Usuário com ID {user_id} não encontrado para atualização.")
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar usuário para atualização: {str(e)}")
            raise e

    @staticmethod
    def list_users():
        """
        Lista todos os usuários do banco de dados.

        Retorna:
            list: Lista de dicionários contendo os dados dos usuários.
        """
        try:
            logger.info("Listando todos os usuários.")
            query = text(
                """
                SELECT id, name, birth_date, cpf, email, time_created, time_updated
                FROM Users
            """
            )
            result = db.session.execute(query).fetchall()
            users = [dict(row._mapping) for row in result]
            logger.info(f"{len(users)} usuário(s) encontrado(s).")
            return users
        except Exception as e:
            logger.error(f"Erro ao listar usuários: {str(e)}")
            raise e

    @staticmethod
    def delete_user(user_id):
        """
        Exclui um usuário pelo ID.

        Parâmetros:
            user_id (string): ID do usuário a ser excluído.
        """
        try:
            logger.info(f"Deletando usuário com ID: {user_id}")
            query = "DELETE FROM Users WHERE id = :id"
            UserRepository._execute_query(query, {"id": user_id})
            logger.info(f"Usuário com ID {user_id} deletado com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao deletar usuário: {str(e)}")
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
            logger.info(f"Executando query: {query}")
            db.session.execute(text(query), data)
            db.session.commit()
            logger.info("Query executada e commitada com sucesso.")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao executar query: {str(e)}")
            raise e

    @staticmethod
    def _formater_data(user_data):
        """
        Formata os dados do usuário para a query de atualização.

        Parâmetros:
            user_data (dict): Dados do usuário a serem formatados.

        Retorna:
            tuple: Dados filtrados e cláusulas SET formatadas para a query.
        """
        filtered_data = {
            key: value for key, value in user_data.items() if value is not None
        }
        set_clauses = ", ".join(
            f"{key} = :{key}" for key in filtered_data if key != "id"
        )
        logger.info(f"Dados formatados para atualização: {filtered_data}")
        return filtered_data, set_clauses
