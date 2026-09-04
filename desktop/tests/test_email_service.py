"""Testes do serviço de envio de email de recuperação de senha."""
import smtplib
from unittest.mock import MagicMock, patch

import pytest

from services.email_service import EmailError, EmailService, montar_link_recuperacao


@pytest.fixture
def email_service():
    return EmailService(
        host="smtp.exemplo.com", port=587, user="app@exemplo.com", senha="segredo"
    )


class TestMontarLinkRecuperacao:
    def test_monta_link_com_token(self):
        link = montar_link_recuperacao("abc123")
        assert link.endswith("/reset?token=abc123")


class TestEnviarEmailRecuperacao:
    def test_envia_email_com_sucesso(self, email_service):
        smtp_mock = MagicMock()
        smtp_instance = smtp_mock.return_value.__enter__.return_value

        with patch("services.email_service.smtplib.SMTP", smtp_mock):
            resultado = email_service.enviar_email_recuperacao(
                "cliente@teste.com", "token-xyz"
            )

        assert resultado is True
        smtp_instance.starttls.assert_called_once()
        smtp_instance.login.assert_called_once_with("app@exemplo.com", "segredo")
        smtp_instance.send_message.assert_called_once()

        mensagem_enviada = smtp_instance.send_message.call_args[0][0]
        assert mensagem_enviada["To"] == "cliente@teste.com"
        assert "token-xyz" in mensagem_enviada.get_content()

    def test_erro_smtp_gera_email_error(self, email_service):
        smtp_mock = MagicMock()
        smtp_mock.return_value.__enter__.side_effect = smtplib.SMTPException(
            "falha de conexão"
        )

        with patch("services.email_service.smtplib.SMTP", smtp_mock):
            with pytest.raises(EmailError):
                email_service.enviar_email_recuperacao("cliente@teste.com", "token-xyz")

    def test_erro_os_error_gera_email_error(self, email_service):
        smtp_mock = MagicMock()
        smtp_mock.return_value.__enter__.side_effect = OSError("host inacessível")

        with patch("services.email_service.smtplib.SMTP", smtp_mock):
            with pytest.raises(EmailError):
                email_service.enviar_email_recuperacao("cliente@teste.com", "token-xyz")
