import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()  # Carregar as variáveis de ambiente do arquivo .env


class Server:
    def __init__(self):
        self.app = Flask(__name__)

        # Certifique-se de que DATABASE_URL foi configurado corretamente
        db_uri = os.getenv(
            "DATABASE_URL", "sqlite:///default.db"
        )  # Valor padrão em caso de falha

        self.app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
        self.app.config["PROPAGATE_EXCEPTIONS"] = True
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    def run(self):
        self.app.run(port=5000, debug=True, host="0.0.0.0")


server = Server()
