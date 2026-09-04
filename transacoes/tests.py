from django.test import SimpleTestCase

from clientes.models import Cliente
from estoque.models import Produto
from fornecedores.models import Fornecedor
from usuarios.models import Usuario

from .models import Transacao


class ModelosMongoEngineTests(SimpleTestCase):
    """Garante que os Documents do MongoEngine e seus relacionamentos funcionam."""

    databases = []

    def setUp(self):
        Transacao.drop_collection()
        Produto.drop_collection()
        Fornecedor.drop_collection()
        Cliente.drop_collection()
        Usuario.drop_collection()
        self.addCleanup(Transacao.drop_collection)
        self.addCleanup(Produto.drop_collection)
        self.addCleanup(Fornecedor.drop_collection)
        self.addCleanup(Cliente.drop_collection)
        self.addCleanup(Usuario.drop_collection)

    def test_modelos_e_relacionamentos_em_portugues(self):
        usuario = Usuario.objects.create(username="maria", nome="Maria")
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

        self.assertEqual(Usuario.objects.get(id=usuario.id).username, "maria")
        self.assertEqual(Cliente.objects.get(id=cliente.id).usuario, usuario)
        self.assertEqual(Fornecedor.objects.get(id=fornecedor.id).nome, "Fornecedor")
        self.assertEqual(Produto.objects.get(id=produto.id).fornecedor, fornecedor)
        self.assertEqual(str(transacao), "Saída - Vestido (1)")
