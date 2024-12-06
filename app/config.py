import os
from flask import Flask


class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL', 'sqlite:///default.db')
        self.app.config["PROPAGATE_EXCEPTIONS"] = True
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    def run(self):
        self.app.run(port=5000, debug=True, host="0.0.0.0")


server = Server()
