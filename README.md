# brecho-manager

Projeto inicial de gerenciamento de brechó usando Django.

## Configuração local

Requisitos: Python 3.10 ou superior.

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # opcional; configure as variáveis conforme necessário
python manage.py migrate
python manage.py runserver
```

Abra `http://127.0.0.1:8000/` no navegador. O banco de dados padrão é SQLite
(`db.sqlite3`).

Para gerar uma chave segura para outros ambientes, defina `DJANGO_SECRET_KEY`.
`DJANGO_DEBUG` aceita `True`/`False` (ou `1`/`0`), e os hosts podem ser
informados em `DJANGO_ALLOWED_HOSTS`, separados por vírgulas.