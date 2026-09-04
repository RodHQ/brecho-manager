from brecho_manager.testing import MongoTestCase

from .models import Usuario


class UsuarioModelTests(MongoTestCase):
    def tearDown(self):
        Usuario.objects.delete()

    def test_criacao_e_hash_de_senha(self):
        usuario = Usuario(username="maria", email="maria@example.com", nome="Maria")
        usuario.set_password("segredo123")
        usuario.save()

        self.assertTrue(usuario.check_password("segredo123"))
        self.assertFalse(usuario.check_password("errada"))
        self.assertEqual(str(usuario), "Maria")
        self.assertEqual(Usuario.objects.count(), 1)

    def test_str_usa_username_quando_nome_vazio(self):
        usuario = Usuario(username="joao", email="joao@example.com")
        usuario.set_password("segredo123")
        usuario.save()

        self.assertEqual(str(usuario), "joao")
