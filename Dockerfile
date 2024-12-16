# Usando uma imagem base do Python
FROM python:3.9-slim

# Definindo diretório de trabalho dentro do container
WORKDIR /app

# Copiando os arquivos do projeto para dentro do container
COPY . /app

# Instalando as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expondo a porta do Flask
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["flask", "run", "--host=0.0.0.0"]
