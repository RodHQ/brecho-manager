from datetime import datetime

import mongoengine as me


class Fornecedor(me.Document):
    """Fornecedor de produtos para o brechó."""

    nome = me.StringField(verbose_name="Nome", max_length=150, required=True)
    email = me.EmailField(verbose_name="Email", required=False)
    telefone = me.StringField(verbose_name="Telefone", max_length=20, default="")
    endereco = me.StringField(verbose_name="Endereço", max_length=255, default="")
    cnpj = me.StringField(verbose_name="CNPJ", max_length=18, required=True, unique=True)
    contato = me.StringField(verbose_name="Contato", max_length=150, default="")
    ativo = me.BooleanField(verbose_name="Ativo", default=True)
    data_cadastro = me.DateTimeField(verbose_name="Data de cadastro", default=datetime.utcnow)

    meta = {
        "collection": "fornecedores",
        "ordering": ["nome"],
    }

    def __str__(self):
        return self.nome
