"""Tela de redefinição de senha usando um token de recuperação (PyQt6)."""
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from services.recovery_service import RecoveryError, RecoveryService
from utils.styles import get_theme
from utils.validators import (
    is_not_empty,
    passwords_match,
    validate_password_strength,
)


class ResetPasswordWindow(QWidget):
    """Janela para o usuário informar o token e definir a nova senha."""

    def __init__(self, token=None, recovery_service=None):
        super().__init__()
        self.recovery_service = recovery_service or RecoveryService()
        self._build_ui()
        if token:
            self.token_input.setText(token)

    def _build_ui(self):
        self.setWindowTitle("Redefinir senha")
        self.setMinimumWidth(360)
        self.setStyleSheet(get_theme(dark_mode=False))

        layout = QVBoxLayout()
        layout.setSpacing(12)

        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("Token de recuperação")
        layout.addWidget(self.token_input)

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Nova senha")
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.new_password_input)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirme a nova senha")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_password_input)

        self.feedback_label = QLabel("")
        self.feedback_label.setWordWrap(True)
        layout.addWidget(self.feedback_label)

        self.reset_button = QPushButton("Redefinir senha")
        self.reset_button.clicked.connect(self.handle_reset)
        layout.addWidget(self.reset_button)

        self.setLayout(layout)

    def handle_reset(self):
        token = self.token_input.text().strip()
        nova_senha = self.new_password_input.text()
        confirmacao = self.confirm_password_input.text()

        if not is_not_empty(token):
            self._set_feedback("Informe o token de recuperação.", success=False)
            return

        valido, mensagem = validate_password_strength(nova_senha)
        if not valido:
            self._set_feedback(mensagem, success=False)
            return

        if not passwords_match(nova_senha, confirmacao):
            self._set_feedback("As senhas informadas não coincidem.", success=False)
            return

        try:
            self.recovery_service.redefinir_senha(token, nova_senha)
        except RecoveryError as exc:
            self._set_feedback(str(exc), success=False)
            return

        self._set_feedback("Senha redefinida com sucesso!", success=True)

    def _set_feedback(self, message, success):
        self.feedback_label.setObjectName("successLabel" if success else "errorLabel")
        self.feedback_label.style().unpolish(self.feedback_label)
        self.feedback_label.style().polish(self.feedback_label)
        self.feedback_label.setText(message)
        if not success:
            QMessageBox.warning(self, "Aviso", message)
