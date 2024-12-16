# User Management API

Este projeto é uma API de gerenciamento de usuários construída com Flask. A API permite criar, atualizar, listar e excluir usuários. Além disso, possui validações para CPF e e-mail, garantindo a integridade dos dados.

## Requisitos

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-RESTx

## Instalação

Para instalar e configurar o ambiente, siga os passos abaixo:

1. Clone o repositório:

```sh
git clone https://github.com/seu-usuario/user-management-api.git
cd user-management-api
````
2 . Crie um ambiente virtual:

```sh
python -m venv venv
source venv/bin/activate  # No Windows use `venv\Scripts\activate`
```
3. Instale as dependências:

```sh
pip install -r requirements.txt
```
**Configuração**
Certifique-se de configurar seu banco de dados no arquivo config.py ou variáveis de ambiente (.env), conforme o caminho do seu computador. Por exemplo:

```sh
SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/instance/database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
````
Uso
Para iniciar o servidor, execute:

```sh
python.app
````
A API estará disponível em http://127.0.0.1:5000.

5. Endpoints
Criação de Usuário
```sh
POST /api/users/
```
Exemplo de Payload:
```sn
json
{
    "name": "João Silva",
    "cpf": "123.456.789-10",
    "email": "joao.silva@example.com",
    "birth_date": "15/08/1990",
    "password_hash": "senhaSegura123"
}
```

**Atualização de Usuário**
```sh
PUT /api/users/<id>
```
Exemplo de Payload:

```sn
json
{
    "name": "João Silva",
    "cpf": "123.456.789-10",
    "email": "joao.silva@example.com",
    "birth_date": "15/08/1990",
    "password_hash": "senhaSegura123"
}
```

**Listagem de Usuários**
```sh
GET /api/users/
```

**Obtenção de Usuário**
```sh
GET /api/users/<id>
```

**Exclusão de Usuário**
```sh
DELETE /api/users/<id>
```

**Limites de Taxa**
A API implementa limites de taxa para evitar abuso. Por padrão, cada endpoint tem um limite de 5 requisições por minuto. Se excedido, a seguinte mensagem será retornada:

```sn
json
{
    "error": "Limite de requisições excedido. Por favor, aguarde e tente novamente em breve."
}
```

**Swagger**
A documentação da API é gerada automaticamente usando Swagger. Para acessar a documentação interativa, vá para:
http://127.0.0.1:5000/

**Docker**
Você pode usar Docker para executar a aplicação em um contêiner. Para isso, siga os passos abaixo:

Construa a imagem Docker:

```sh
docker build -t user-management-api .
```

Execute o contêiner:

```sh
docker run -d -p 5000:5000 user-management-api
```
A API estará disponível em http://127.0.0.1:5000.

**Observações**

`CPF`: O CPF deve ser real e válido. A API verifica a unicidade do CPF no sistema.

`Email`: O e-mail deve ser único e válido. A API verifica a unicidade do e-mail no sistema.

`Senha`: A senha deve ter 8 digitos, sendo pelo menos 1 numero e 1 letra.

**Estrutura do Projeto**

`app/`: Contém o código principal da aplicação

`controllers/`: Controladores da API

`models/`: Modelos do banco de dados

`repositories/`: Camada de acesso a dados

`schemas/`: Esquemas de validação de dados

`services/`: Camada de serviços

`utils/`: Utilitários e helpers

`tests/`: Testes automatizados

**Criação de Massa para o banco de dados**
O script para inserção de dados está no arquivo `inserts_banco.py`

Passos para Executar
Ative seu ambiente virtual:
```sh
venv/Scripts/activate
```
Execute o script:
```sh
python inserts_banco.py
```
**Contato**
Se tiver alguma dúvida ou sugestão, entre em contato:


Linkedin: [mariachiquezi](https://www.linkedin.com/in/maria-eduarda-chiquezi/)
