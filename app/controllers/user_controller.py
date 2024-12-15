from flask import request, jsonify
from app.services.user_service import UserService
from app.exceptions.error_handler import ErrorHandler

class UserController:

    @staticmethod
    def create_user(data):
        try:
            user_service = UserService()
            print("oi controlle")
            response, status_code = user_service.create_user(data)
            return response, status_code
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    @staticmethod
    def list_users():
        try:
            user_service = UserService()
            return user_service.list_users()
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    @staticmethod
    def get_user(id):
        try:
            user_service = UserService()
            response, status_code = user_service.get_user(id)
            print("responde", response)
            print(status_code)
            return response, status_code
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)


    @staticmethod
    def update_user(id, data):
        try:
            user_service = UserService()
            response, status_code = user_service.update_user(id, data)
            return response, status_code
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    @staticmethod
    def delete_user(id):
        try:
            user_service = UserService()
            response, status_code = user_service.delete_user(id)
            return response, status_code
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)
