from brecho_manager.testing import MongoTestCase

from .models import Fornecedor


class FornecedorModelTests(MongoTestCase):
    def tearDown(self):
        Fornecedor.objects.delete()

    def test_criacao_de_fornecedor(self):
        fornecedor = Fornecedor.objects.create(nome="Fornecedor Teste", cnpj="12345678000199")

        self.assertEqual(str(fornecedor), "Fornecedor Teste")
        self.assertTrue(fornecedor.ativo)
        self.assertEqual(Fornecedor.objects.count(), 1)
