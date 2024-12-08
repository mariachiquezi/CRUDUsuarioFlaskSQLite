from app import create_app
from db import db


def init_db():
    app = create_app()
    with app.app_context():
        try:
            db.create_all()
            print("Tabelas criadas com sucesso!")
        except Exception as e:
            print(f"Erro ao criar tabelas: {e}")


if __name__ == "__main__":
    init_db()
