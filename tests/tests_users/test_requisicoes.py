import pytest
from app.models.user_model import UserModel


def test_create_user(client, fake_user):
    response = client.post("/usuarios", json=fake_user)
    print(response.json)  # Debug print
    assert response.status_code == 201
    assert "message" in response.json

    # Verificação da criação do usuário no banco de dados
    with client.application.app_context():
        user = UserModel.query.filter_by(email=fake_user["email"]).first()
        assert user is not None
        assert user.email == fake_user["email"]


def test_get_user_not_found(client):
    response = client.get("/usuarios/999")
    assert response.status_code == 404
    assert "message" in response.json
    assert response.json["message"] == "Usuário não encontrado"


def test_update_user(client, fake_user):
    response = client.post("/usuarios", json=fake_user)
    print(response.json)  # Debug print
    assert response.status_code == 201

    # Verificação da criação do usuário no banco de dados
    with client.application.app_context():
        user = UserModel.query.filter_by(email=fake_user["email"]).first()
        assert user is not None

    update_data = {"name": "João da Silva"}
    response = client.put(f"/usuarios/{user.id}", json=update_data)
    print(response.json)  # Debug print
    assert response.status_code == 200
    assert "message" in response.json
    assert response.json["message"] == "Usuário atualizado com sucesso!"


def test_delete_user(client, fake_user):
    response = client.post("/usuarios", json=fake_user)
    print(response.json)  # Debug print
    assert response.status_code == 201

    # Verificação da criação do usuário no banco de dados
    with client.application.app_context():
        user = UserModel.query.filter_by(email=fake_user["email"]).first()
        assert user is not None

    response = client.delete(f"/usuarios/{user.id}")
    print(response.json)  # Debug print
    assert response.status_code == 200
    assert "message" in response.json
    assert response.json["message"] == "Usuário deletado com sucesso!"


def test_rate_limit(client):
    for _ in range(5):
        client.get("/usuarios")

    response = client.get("/usuarios")
    print(response.json)  # Debug print
    assert response.status_code == 429
    assert "error" in response.json
    assert (
        response.json["error"]
        == "429 Too Many Requests: Limite de requisições excedido. Por favor, aguarde e tente novamente em breve."
    )
