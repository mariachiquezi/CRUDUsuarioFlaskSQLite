from flask import request, jsonify
from app.services.user_service import UserService
from app.exceptions.error_handler import ErrorHandler
from app.exceptions.validation_error import ValidationError
from app.exceptions.database_error import UniqueConstraintError


class UserController:

    @staticmethod
    def create_user():
        try:
            data = request.json
            response, status_code = UserService().create_user(data)
            return jsonify(response), status_code
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except UniqueConstraintError as e:
            return ErrorHandler.handle_unique_constraint_error(e)

    @staticmethod
    def list_users():
        try:
            response = UserService().list_users()
            return jsonify(response)
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    @staticmethod
    def get_user(id):
        try:
            response, status_code = UserService().get_user(id)
            return jsonify(response), status_code
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)

    @staticmethod
    def update_user(id):
        try:
            data = request.json
            response, status_code = UserService().update_user(id, data)
            return jsonify(response), status_code
        except ValidationError as e:
            return ErrorHandler.handle_validation_error(e)
        except UniqueConstraintError as e:
            return ErrorHandler.handle_unique_constraint_error(e)

    @staticmethod
    def delete_user(id):
        try:
            response, status_code = UserService().delete_user(id)
            return jsonify(response), status_code
        except Exception as e:
            return ErrorHandler.handle_generic_error(e)
