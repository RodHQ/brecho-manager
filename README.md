# brecho-manager

Projeto inicial de gerenciamento de brechó usando Django e MongoDB (via
MongoEngine).

## Configuração local

Requisitos: Python 3.10 ou superior e uma instância do MongoDB acessível
(local ou em contêiner).

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # configure as variáveis de conexão com o MongoDB
python manage.py runserver
```

Abra `http://127.0.0.1:8000/` no navegador. O banco de dados é o **MongoDB**,
acessado através do MongoEngine — não há SQLite nem migrações do Django ORM.

Para gerar uma chave segura para outros ambientes, defina `DJANGO_SECRET_KEY`.
`DJANGO_DEBUG` aceita `True`/`False` (ou `1`/`0`), e os hosts podem ser
informados em `DJANGO_ALLOWED_HOSTS`, separados por vírgulas.

A conexão com o MongoDB é configurada pelas variáveis `MONGO_DB_NAME`,
`MONGO_HOST`, `MONGO_PORT`, `MONGO_USERNAME`, `MONGO_PASSWORD` e
`MONGO_AUTHENTICATION_SOURCE` (veja `.env.example`).
