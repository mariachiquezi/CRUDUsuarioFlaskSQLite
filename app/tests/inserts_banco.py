# import os
# import random
# import bcrypt
# import hashlib
# import sys
# import time
# from faker import Faker
# from cpf_generator import CPF
# from datetime import datetime, timedelta
# from sqlalchemy import create_engine, text

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# from app.services.users_validator.password_validator_service import PasswordService
# from app.utils.id_generator import (
#     generate_unique_id,
# )  # Agora este import será encontrado

# # Configuração do SQLite
# DATABASE_URI = "sqlite:///instance/users_database.db"  # Altere o nome do arquivo SQLite, se necessário
# engine = create_engine(DATABASE_URI)

# fake = Faker("pt_BR")


# def generate_password_hash(password):
#     """
#     Gera um hash para a senha usando bcrypt.
#     """
#     password_bytes = password.encode("utf-8")  # Garantir a codificação correta
#     salt = bcrypt.gensalt()
#     return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


# def random_birth_date():
#     """
#     Gera uma data de nascimento aleatória entre 1950 e 2005.
#     """
#     start_date = datetime(1950, 1, 1)
#     end_date = datetime(2005, 12, 31)
#     random_date = start_date + timedelta(
#         days=random.randint(0, (end_date - start_date).days)
#     )
#     return random_date.strftime("%Y-%m-%d")


# def generate_user_data():
#     """
#     Gera dados para um usuário.
#     """
#     name = fake.name()
#     email = fake.email()
#     cpf = CPF.generate()
#     id = generate_unique_id(cpf)
#     birth_date = random_birth_date()
#     time_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     time_updated = time_created
#     password = fake.password(
#         length=8, special_chars=False, digits=True, upper_case=True, lower_case=True
#     )
#     password_hash = generate_password_hash(password)

#     return {
#         "id": id,
#         "name": name,
#         "email": email,
#         "cpf": cpf,
#         "birth_date": birth_date,
#         "time_created": time_created,
#         "time_updated": time_updated,
#         "password_hash": password_hash,
#     }


# def insert_user_to_db(user_data):
#     """
#     Insere um usuário no banco de dados.
#     """
#     query = text(
#         """
#         INSERT INTO Users (id, name, email, cpf, birth_date, time_created, time_updated, password_hash)
#         VALUES (:id, :name, :email, :cpf, :birth_date, :time_created, :time_updated, :password_hash)
#         """
#     )
#     with engine.connect() as connection:
#         # Passa os dados como um dicionário e usa params
#         connection.execute(query, user_data)
#         connection.commit()



# if __name__ == "__main__":
#     n = 1000  # Teste com um número reduzido de registros
#     print("Iniciando a inserção no banco de dados...")

#     start_time = time.time()  # Marca o início do processo

#     for i in range(n):
#         user_data = generate_user_data()
#         try:
#             insert_user_to_db(user_data)
#             if (i + 1) % 10 == 0:  # Exibe progresso a cada 10 registros
#                 print(f"{i + 1} registros inseridos...")
#         except Exception as e:
#             print(f"Erro ao inserir registro {i + 1}: {e}")

#     end_time = time.time()  # Marca o fim do processo

#     total_seconds = end_time - start_time
#     total_minutes = total_seconds / 60

#     print(
#         f"Processo concluído em {total_seconds:.2f} segundos ({total_minutes:.2f} minutos)!"
#     )
