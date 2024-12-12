from faker import Faker
import pytest
from app import create_app, db


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"}
    )
    return app


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown(app):
    with app.app_context():
        db.create_all()
    yield
    with app.app_context():
        db.session.close_all()  # Close all sessions to avoid issues
        for table in reversed(db.metadata.sorted_tables):
            print(f"Dropping table {table}")  # Debug print
            db.metadata.remove(
                table
            )  # Remove table from metadata to avoid duplication issues
        db.drop_all()  # Drop all tables completely


@pytest.fixture
def fake_user():
    fake = Faker("pt_BR")
    return {
        "name": fake.name(),
        "email": fake.email(),
        "cpf": fake.cpf(),  # Gera um CPF único
        "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=90).strftime(
            "%d-%m-%Y"
        ),
        "password_hash": fake.password(),
    }
