from pydantic import BaseModel, EmailStr
from typing import Optional


class UserSchema(BaseModel):
    email: EmailStr
    name: str
    password_hash: str
    cpf: str
    birth_date: str  # Pode ser datetime ou outro formato, se necessário

    # Validação do CPF ou outras regras podem ser adicionadas aqui
    class Config:
        orm_mode = True
