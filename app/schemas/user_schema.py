from app.utils.format_date import CustomDateField
from db import db
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.user_model import UserModel
from datetime import datetime


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True
        sqla_session = db.session

    id = fields.String(required=False)
    birth_date = CustomDateField()


user_schema = UserSchema()
users_schema = UserSchema(many=True)
