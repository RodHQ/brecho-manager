from brecho_manager.testing import MongoTestCase

from usuarios.models import Usuario

from .models import Cliente


class ClienteModelTests(MongoTestCase):
    def tearDown(self):
        Cliente.objects.delete()
        Usuario.objects.delete()

    def test_criacao_de_cliente_com_usuario_responsavel(self):
        usuario = Usuario(username="maria", email="maria@example.com", nome="Maria")
        usuario.set_password("segredo123")
        usuario.save()

        cliente = Cliente.objects.create(
            nome="Ana",
            cpf_cnpj="12345678901",
            usuario=usuario,
        )

        self.assertEqual(str(cliente), "Ana")
        self.assertEqual(cliente.usuario, usuario)
        self.assertEqual(Cliente.objects(usuario=usuario).count(), 1)
