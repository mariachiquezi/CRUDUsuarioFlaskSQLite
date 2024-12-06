import re
from datetime import datetime
from db import db
from sqlalchemy.sql import func
from db import db
from app.config import server


class UserModel(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.String(20), primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    age = db.Column(db.String(3))
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    password_hash = db.Column(db.Text, nullable=False)

    def __init__(self, name, email, age, cpf, password_hash):
        self.name = name
        self.email = email
        self.cpf = cpf
        self.age = age
        self.password_hash = password_hash

        print("id", self.id)
        print("senha", self.password_hash)

    def as_dict(self):
        """Converte o objeto UserModel para um dicionário."""
        return { 
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "time_created": self.time_created,
            "time_updated": self.time_updated,
        }

    def __repr__(self):
        """Representação legível do objeto."""
        return f"<User {self.name}, {self.email}>"
