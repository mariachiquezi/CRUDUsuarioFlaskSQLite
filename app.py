from flask import Flask
from db import db
from app.controllers.user_controller import user_bp
from app.config import server

app = server.app

db.init_app(app)


# Inicializa o banco de dados
def init_db():
    with app.app_context():
        try:
            db.create_all()
            print("Tabelas criadas com sucesso!")
        except Exception as e:
            print(f"Erro ao criar tabelas: {e}")


# Configuração do banco de dados
init_db()

# Registro do Blueprint
app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True)
