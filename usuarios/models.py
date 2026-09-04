from datetime import datetime

import mongoengine as me


class Usuario(me.Document):
    """Usuário customizado do sistema, modelado como Document do MongoEngine.

    A senha deve ser gerenciada manualmente (por exemplo, com
    `django.contrib.auth.hashers.make_password`), já que este Document não
    está integrado ao `django.contrib.auth`.
    """

    username = me.StringField(verbose_name="Usuário", max_length=150, required=True, unique=True)
    nome = me.StringField(verbose_name="Nome", max_length=150, default="")
    email = me.EmailField(verbose_name="Email", required=False)
    senha = me.StringField(verbose_name="Senha (hash)", default="")
    telefone = me.StringField(verbose_name="Telefone", max_length=20, default="")
    data_criacao = me.DateTimeField(verbose_name="Data de criação", default=datetime.utcnow)
    ativo = me.BooleanField(verbose_name="Ativo", default=True)
    is_staff = me.BooleanField(verbose_name="Membro da equipe", default=False)
    is_superuser = me.BooleanField(verbose_name="Superusuário", default=False)

    meta = {
        "collection": "usuarios",
        "ordering": ["username"],
    }

    def __str__(self):
        return self.nome or self.username
