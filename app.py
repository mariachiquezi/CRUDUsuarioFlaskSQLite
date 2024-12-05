from flask import Flask
from db import db
from app.blueprints.user_blueprint import user_bp
from app.config import server

app = server.app

db.init_app(app)

# Criação das tabelas no banco de dados
with app.app_context():
    try:
        db.create_all()
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")

# Registro do Blueprint
app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True)
