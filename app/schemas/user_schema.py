from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserSchema(BaseModel):
    id: str
    cpf: str  # CPF validado no ValidatorService, sem validação adicional aqui
    email: EmailStr
    password_hash: str
    time_created: datetime
    time_updated: datetime

    class Config:
        orm_mode = True


class UserCreateSchema(BaseModel):
    name: str  # Incluído para a criação de usuário
    cpf: str  # Apenas aceita como string; validação acontece no ValidatorService
    email: EmailStr
    password_hash: str


class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr]
    password_hash: Optional[str]
