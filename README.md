# brecho-manager

Projeto inicial de gerenciamento de brechó usando Django e MongoDB.

## Banco de dados: MongoDB via Docker Compose

O projeto usa o [MongoDB](https://www.mongodb.com/) como banco de dados,
acessado pela aplicação através do [MongoEngine](https://mongoengine.org/).
O MongoDB e o [Mongo Express](https://github.com/mongo-express/mongo-express)
(interface visual para administrar o banco) sobem via Docker Compose.

Requisitos: Docker e Docker Compose, além de Python 3.10 ou superior.

```bash
# 1. Configure as variáveis de ambiente
cp .env.example .env            # ajuste usuário/senha/host conforme necessário

# 2. Suba o MongoDB e o Mongo Express
docker compose up -d

# 3. Instale as dependências Python e rode a aplicação
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

Abra `http://127.0.0.1:8000/` no navegador.

### Acessando o MongoDB via Mongo Express

Com os contêineres em execução, acesse `http://localhost:8081/` e entre com
o mesmo usuário/senha definidos em `MONGO_USERNAME`/`MONGO_PASSWORD` (no
`.env`). Por ele é possível navegar pelas coleções, documentos e índices do
banco `brecho_manager` de forma visual.

> Se você rodar a aplicação Django diretamente na sua máquina (fora de um
> contêiner), defina `MONGO_HOST=localhost` no seu `.env`, já que o valor
> `mongodb` só é resolvível dentro da rede do Docker Compose.

### Comandos Docker úteis

```bash
docker compose up -d          # sobe MongoDB e Mongo Express em segundo plano
docker compose ps             # lista os contêineres e seus status
docker compose logs -f mongodb  # acompanha os logs do MongoDB
docker compose down           # para e remove os contêineres (mantém o volume)
docker compose down -v        # para os contêineres e apaga o volume de dados
```

Os dados do MongoDB são persistidos no volume Docker `mongodb_data`.

## Variáveis de ambiente

| Variável | Descrição |
| --- | --- |
| `DJANGO_SECRET_KEY` | Chave secreta do Django. Defina um valor seguro em produção. |
| `DJANGO_DEBUG` | Aceita `True`/`False` (ou `1`/`0`). |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos, separados por vírgulas. |
| `MONGO_USERNAME` | Usuário root do MongoDB (usado pelo contêiner e pela conexão do Django). |
| `MONGO_PASSWORD` | Senha do usuário root do MongoDB. |
| `MONGO_DB` | Nome do banco de dados usado pela aplicação. |
| `MONGO_HOST` | Host do MongoDB (`mongodb` no Docker Compose, `localhost` fora dele). |
| `MONGO_PORT` | Porta do MongoDB (padrão `27017`). |

## Observações sobre o Django Admin

Os modelos de domínio (`usuarios`, `clientes`, `fornecedores`, `estoque`,
`transacoes`) são `Document`s do MongoEngine, não `Model`s do Django ORM, e
por isso não podem ser registrados no Django Admin. Não há banco de dados
relacional configurado (`DATABASES = {}`), então recursos que dependem dele,
como autenticação padrão do `django.contrib.auth` e sessões, não funcionam
sem configuração adicional. Para gerenciar os dados visualmente, utilize o
Mongo Express.
