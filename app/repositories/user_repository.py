from sqlalchemy import text
from datetime import datetime
from db import db
import pytz

# Supondo que você tenha uma classe DateTimeUtils com o método convert_to_timezone.
from app.utils.format import DateTimeUtils  # Importa a classe onde está a função de conversão


class UserRepository:

    def create_user(user_data):
        query = text(
            """
            INSERT INTO Users (id, name, birth_date, cpf, email, password_hash, time_created, time_updated)
            VALUES (:id, :name, :birth_date, :cpf, :email, :password_hash, :time_created, :time_updated)
            """
        )
        UserRepository.save_to_db(query, user_data)

    def update_user(user_data):
        query = text(
            """
            UPDATE Users
            SET name = :name, birth_date = :birth_date, cpf = :cpf, email = :email, password_hash = :password_hash, time_updated = :time_updated
            WHERE id = :id
            """
        )
        # Converte as datas para o fuso horário de Brasília
        user_data = DateTimeUtils.adjust_times_for_dict(
            user_data, target_timezone="America/Sao_Paulo"
        )
        UserRepository.save_to_db(query, user_data)

    def get_user(user_id):
        query = text(
            """
            SELECT id, name, birth_date, cpf, email, time_created, time_updated
            FROM Users WHERE id = :id
            """
        )
        result = db.session.execute(query, {"id": user_id}).fetchone()
        
        return result

    def list_users():
        query = text(
            """
            SELECT id, name, birth_date, cpf, email, time_created, time_updated
            FROM Users
            """
        )
        result = db.session.execute(query).fetchall()
        return [dict(row._mapping) for row in result]

    def delete_user(user_id):
        query = text("DELETE FROM Users WHERE id = :id")
        db.session.execute(query, {"id": user_id})
        db.session.commit()

    def save_to_db(query, data):
        try:
            # Garantir que as datas sejam convertidas antes de salvar no banco
            db.session.execute(query, data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
