from django.test import TestCase

from clientes.models import Cliente
from estoque.models import Produto
from fornecedores.models import Fornecedor
from usuarios.models import Usuario

from .models import Transacao


class ModelosEmPortuguesTests(TestCase):
    def test_modelos_e_relacionamentos_em_portugues(self):
        usuario = Usuario.objects.create_user(username="maria", nome="Maria")
        cliente = Cliente.objects.create(
            nome="Ana",
            cpf_cnpj="12345678901",
            usuario=usuario,
        )
        fornecedor = Fornecedor.objects.create(nome="Fornecedor", cnpj="12345678000199")
        produto = Produto.objects.create(
            nome="Vestido",
            sku="VEST-001",
            preco="99.90",
            quantidade=2,
            fornecedor=fornecedor,
        )
        transacao = Transacao.objects.create(
            tipo=Transacao.TIPO_SAIDA,
            cliente=cliente,
            fornecedor=fornecedor,
            produto=produto,
            quantidade=1,
            valor="99.90",
        )

        self.assertEqual(usuario._meta.label, "usuarios.Usuario")
        self.assertEqual(cliente._meta.label, "clientes.Cliente")
        self.assertEqual(fornecedor._meta.label, "fornecedores.Fornecedor")
        self.assertEqual(produto._meta.label, "estoque.Produto")
        self.assertEqual(transacao._meta.label, "transacoes.Transacao")
        self.assertEqual(str(transacao), "Saída - Vestido (1)")
