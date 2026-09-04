from brecho_manager.testing import MongoTestCase
from clientes.models import Cliente
from estoque.models import Produto
from fornecedores.models import Fornecedor
from usuarios.models import Usuario

from .models import Transacao


class ModelosEmPortuguesTests(MongoTestCase):
    def tearDown(self):
        Transacao.objects.delete()
        Produto.objects.delete()
        Cliente.objects.delete()
        Fornecedor.objects.delete()
        Usuario.objects.delete()

    def test_modelos_e_relacionamentos_em_portugues(self):
        usuario = Usuario(username="maria", email="maria@example.com", nome="Maria")
        usuario.set_password("segredo123")
        usuario.save()
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

        self.assertEqual(usuario._collection.name, "usuarios")
        self.assertEqual(cliente._collection.name, "clientes")
        self.assertEqual(fornecedor._collection.name, "fornecedores")
        self.assertEqual(produto._collection.name, "estoque")
        self.assertEqual(transacao._collection.name, "transacoes")
        self.assertEqual(str(transacao), "Saída - Vestido (1)")
