from flask import request, jsonify
from app.exceptions.validation_error import ValidationError
from app.services.user_service import UserService
from app.exceptions.error_handler import ErrorHandler


class UserController:
    @staticmethod
    def create_user(data):
        """
        Cria um novo usuário.

        Parâmetros:
            data (dict): Dados do usuário a serem criados.

        Retorna:
            response (dict): Resposta contendo a mensagem de sucesso ou erro.
            status_code (int): Código de status HTTP.
        """
        try:
            response, status_code = UserService().create_user(data)
            return response, status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def list_users():
        """
        Lista todos os usuários.

        Retorna:
            response (dict): Lista de usuários ou mensagem de erro.
            status_code (int): Código de status HTTP.
        """
        try:
            user_service = UserService()
            return user_service.list_users()
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    @staticmethod
    def get_user(id):
        """
        Obtém um usuário específico pelo ID utilizando o serviço de usuário.

        Parâmetros:
            id (string): ID do usuário a ser obtido.

        Retorna:
            response (dict): Dados do usuário ou mensagem de erro.
            status_code (int): Código de status HTTP.
        """
        try:
            user_service = UserService()
            response, status_code = user_service.get_user(id)
            return response, status_code
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    @staticmethod
    def update_user(id, data):
        """
        Atualiza um usuário específico pelo ID utilizando o serviço de usuário.

        Parâmetros:
            id (string): ID do usuário a ser atualizado.
            data (dict): Dados atualizados do usuário.

        Retorna:
            response (dict): Mensagem de sucesso ou erro.
            status_code (int): Código de status HTTP.
        """
        try:
            user_service = UserService()
            response, status_code = user_service.update_user(id, data)
            return response, status_code
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    @staticmethod
    def delete_user(id):
        """
        Exclui um usuário específico pelo ID.

        Parâmetros:
            id (string): ID do usuário a ser excluído.

        Retorna:
            response (dict): Mensagem de sucesso ou erro.
            status_code (int): Código de status HTTP.
        """
        try:
            user_service = UserService()
            response, status_code = user_service.delete_user(id)
            return response, status_code
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)
