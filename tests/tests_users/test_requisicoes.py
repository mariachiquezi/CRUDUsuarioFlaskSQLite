from app.models.user_model import UserModel


def test_create_user(client, fake_user):
    response = client.post("api/users/", json=fake_user)
    print(response.json)
    assert response.status_code == 201
    assert "message" in response.json

    with client.application.app_context():
        user = UserModel.query.filter_by(email=fake_user["email"]).first()
        assert user is not None
        assert user.email == fake_user["email"]


def test_get_user_not_found(client):
    response = client.get("api/users/999")
    assert response.status_code == 404
    assert "message" in response.json
    assert response.json["message"] == "Usuário não encontrado"


def test_update_user(client, fake_user):
    response = client.post("api/users/", json=fake_user)
    print(response.json)
    assert response.status_code == 201

    with client.application.app_context():
        user = UserModel.query.filter_by(email=fake_user["email"]).first()
        assert user is not None

    update_data = {
        "name": "João da Silva",
        "cpf": fake_user["cpf"],
        "email": fake_user["email"],
        "birth_date": fake_user["birth_date"],
        "password_hash": fake_user["password_hash"],
    }
    response = client.put(f"api/users/{user.id}", json=update_data)
    print(response.json)
    assert response.status_code == 200


def test_delete_user(client, fake_user):
    response = client.post("api/users/", json=fake_user)
    print(response.json)
    assert response.status_code == 201

    with client.application.app_context():
        user = UserModel.query.filter_by(email=fake_user["email"]).first()
        assert user is not None

    response = client.delete(f"api/users/{user.id}")
    assert response.status_code == 200
    assert "message" in response.json
    assert response.json["message"] == "Usuário deletado com sucesso!"


def test_rate_limit(client):
    for _ in range(10):
        client.get("api/users/")

    response = client.get("api/users/")
    assert response.status_code == 429
