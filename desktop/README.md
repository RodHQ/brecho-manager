# Brecho Manager - Aplicação Desktop

Aplicação desktop (PyQt6) com autenticação e recuperação de senha, integrada
ao mesmo banco MongoDB usado pela aplicação Django (collection `usuarios`).

## Funcionalidades

- Login com email/usuário + senha (autenticação contra o MongoDB)
- Token JWT de sessão, válido por 7 dias (armazenado em arquivo local `.token`)
- Recuperação de senha por email, com token de expiração de 24 horas
- Redefinição de senha com validação de força de senha
- Dashboard inicial após o login, com logout

## Instalação

Requisitos: Python 3.10+ e acesso a um MongoDB (o mesmo utilizado pela
aplicação Django, veja o `docker-compose.yml` na raiz do repositório).

```bash
cd desktop
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuração

Copie o arquivo de exemplo e ajuste os valores conforme seu ambiente:

```bash
cp .env.example .env
```

Variáveis disponíveis:

| Variável | Descrição |
| --- | --- |
| `MONGO_URI` | String de conexão do MongoDB |
| `MONGO_DB` | Nome do banco de dados |
| `EMAIL_HOST` / `EMAIL_PORT` | Servidor SMTP usado para envio de emails |
| `EMAIL_USER` / `EMAIL_PASSWORD` | Credenciais da conta de envio (Gmail: use uma senha de app) |
| `RECOVERY_TOKEN_EXPIRY` | Tempo de expiração do token de recuperação (segundos, padrão 86400 = 24h) |
| `JWT_SECRET_KEY` | Chave secreta usada para assinar os tokens JWT |
| `JWT_EXPIRY_DAYS` | Validade do token de sessão em dias (padrão 7) |
| `APP_NAME` | Nome exibido na interface |
| `FRONTEND_URL` | URL usada para montar o link de recuperação de senha |

## Rodando a aplicação

```bash
python main.py
```

## Executando os testes

```bash
pip install pytest
python -m pytest tests/
```

## Gerando um executável com PyInstaller

```bash
pip install pyinstaller
pyinstaller --noconfirm --windowed --name "BrechoManager" main.py
```

O executável gerado ficará disponível em `dist/BrechoManager/`.

## Estrutura de pastas

```
desktop/
├── main.py                       # ponto de entrada
├── requirements.txt
├── .env.example
├── ui/                           # telas (PyQt6)
│   ├── login_window.py
│   ├── recovery_dialog.py
│   ├── reset_password_window.py
│   └── main_window.py
├── services/                     # regras de negócio
│   ├── auth_service.py
│   ├── recovery_service.py
│   └── email_service.py
├── utils/                        # utilitários
│   ├── hash_password.py
│   ├── validators.py
│   ├── config.py
│   └── styles.py
├── models/                       # documentos MongoDB
│   ├── usuario_model.py
│   └── recovery_token_model.py
├── db/
│   └── mongodb_connection.py     # conexão singleton + CRUD
└── tests/
```
