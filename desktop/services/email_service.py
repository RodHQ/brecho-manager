"""Serviço de envio de email (SMTP - Gmail ou SendGrid) para recuperação de senha."""
import smtplib
import ssl
from email.message import EmailMessage

from utils.config import config


class EmailError(Exception):
    """Erro ao enviar email."""


def _montar_corpo_recuperacao(link_recuperacao):
    return (
        f"Olá,\n\n"
        f"Recebemos uma solicitação para redefinir sua senha no {config.APP_NAME}.\n"
        f"Clique (ou copie e cole) no link abaixo para criar uma nova senha:\n\n"
        f"{link_recuperacao}\n\n"
        f"Esse link expira em algumas horas. Se você não solicitou essa alteração, "
        f"ignore este email.\n\n"
        f"Equipe {config.APP_NAME}"
    )


def montar_link_recuperacao(token):
    return f"{config.FRONTEND_URL}/reset?token={token}"


class EmailService:
    def __init__(self, host=None, port=None, user=None, senha=None):
        self.host = host or config.EMAIL_HOST
        self.port = port or config.EMAIL_PORT
        self.user = user or config.EMAIL_USER
        self.senha = senha or config.EMAIL_PASSWORD

    def enviar_email_recuperacao(self, destinatario, token):
        """Envia o email com o link de recuperação de senha para o destinatário."""
        link = montar_link_recuperacao(token)

        mensagem = EmailMessage()
        mensagem["Subject"] = f"{config.APP_NAME} - Recuperação de senha"
        mensagem["From"] = self.user
        mensagem["To"] = destinatario
        mensagem.set_content(_montar_corpo_recuperacao(link))

        try:
            contexto = ssl.create_default_context()
            with smtplib.SMTP(self.host, self.port, timeout=10) as servidor:
                servidor.starttls(context=contexto)
                servidor.login(self.user, self.senha)
                servidor.send_message(mensagem)
        except (smtplib.SMTPException, OSError) as exc:
            raise EmailError(f"Falha ao enviar email de recuperação: {exc}") from exc

        return True
