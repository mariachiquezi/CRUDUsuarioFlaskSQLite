from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.utils.format_date import CustomDateField
from db import db
from marshmallow import fields
from app.models.user_model import UserModel


from marshmallow import validates, ValidationError as MarshmallowValidationError


class UserSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = UserModel
        load_instance = True
        sqla_session = db.session

    @validates("cpf")
    def validate_cpf_length(self, value):
        if len(value) != 11:
            raise MarshmallowValidationError("CPF deve ter 11 dígitos.")

    id = fields.String(required=False)
    birth_date = CustomDateField(required=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
