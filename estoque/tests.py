from brecho_manager.testing import MongoTestCase

from fornecedores.models import Fornecedor

from .models import Produto


class ProdutoModelTests(MongoTestCase):
    def tearDown(self):
        Produto.objects.delete()
        Fornecedor.objects.delete()

    def test_criacao_de_produto_com_fornecedor(self):
        fornecedor = Fornecedor.objects.create(nome="Fornecedor", cnpj="12345678000199")
        produto = Produto.objects.create(
            nome="Vestido",
            sku="VEST-001",
            preco="99.90",
            quantidade=2,
            fornecedor=fornecedor,
        )

        self.assertEqual(str(produto), "Vestido")
        self.assertEqual(produto.fornecedor, fornecedor)
        self.assertEqual(Produto.objects(fornecedor=fornecedor).count(), 1)
