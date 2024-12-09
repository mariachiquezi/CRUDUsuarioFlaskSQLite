from sqlalchemy import Index
from db import db
from sqlalchemy.sql import func


class UserModel(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.String(20), primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False, index=True)  #
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)  #

    cpf = db.Column(db.String(11), unique=True, nullable=False, index=True)  #
    birth_date = db.Column(db.Date, nullable=True)
    time_created = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), index=True
    )  #
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    password_hash = db.Column(db.Text, nullable=False)

    def __init__(self, id, name, email, birth_date, cpf, password_hash):
        self.id = id
        self.name = name
        self.email = email
        self.cpf = cpf
        self.birth_date = birth_date
        self.password_hash = password_hash

        print("id", self.id)
        print("senha", self.password_hash)

    __table_args__ = (
        Index("ix_users_name", "name"),
        Index("ix_users_cpf", "cpf"),
        Index("ix_users_email", "email"),
        Index("ix_users_time_created", "time_created"),
    )

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
