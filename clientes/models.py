from datetime import datetime

import mongoengine as me


class Cliente(me.Document):
    """Cliente do brechó."""

    nome = me.StringField(verbose_name="Nome", max_length=150, required=True)
    email = me.EmailField(verbose_name="Email", required=False)
    telefone = me.StringField(verbose_name="Telefone", max_length=20, default="")
    endereco = me.StringField(verbose_name="Endereço", max_length=255, default="")
    cidade = me.StringField(verbose_name="Cidade", max_length=100, default="")
    cep = me.StringField(verbose_name="CEP", max_length=10, default="")
    cpf_cnpj = me.StringField(verbose_name="CPF/CNPJ", max_length=18, required=True, unique=True)
    data_cadastro = me.DateTimeField(verbose_name="Data de cadastro", default=datetime.utcnow)
    usuario = me.ReferenceField(
        "Usuario",
        verbose_name="Usuário responsável",
        reverse_delete_rule=me.NULLIFY,
        null=True,
    )

    meta = {
        "collection": "clientes",
        "ordering": ["nome"],
    }

    def __str__(self):
        return self.nome
