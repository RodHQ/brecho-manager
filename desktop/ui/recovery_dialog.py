"""Dialog de recuperação de senha (PyQt6)."""
from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from services.recovery_service import RecoveryError, RecoveryService
from utils.styles import get_theme
from utils.validators import is_valid_email


class RecoveryDialog(QDialog):
    """Dialog para solicitar o envio do link de recuperação de senha."""

    def __init__(self, parent=None, recovery_service=None):
        super().__init__(parent)
        self.recovery_service = recovery_service or RecoveryService()
        self._build_ui()

    def _build_ui(self):
        self.setWindowTitle("Recuperar senha")
        self.setMinimumWidth(320)
        self.setStyleSheet(get_theme(dark_mode=False))

        layout = QVBoxLayout()
        layout.setSpacing(12)

        info_label = QLabel(
            "Informe seu email cadastrado para receber o link de recuperação."
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        self.feedback_label = QLabel("")
        self.feedback_label.setWordWrap(True)
        layout.addWidget(self.feedback_label)

        self.send_button = QPushButton("Enviar link de recuperação")
        self.send_button.clicked.connect(self.handle_send)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def handle_send(self):
        email = self.email_input.text().strip()

        if not is_valid_email(email):
            self._set_feedback("Informe um email válido.", success=False)
            return

        self.send_button.setEnabled(False)
        self.send_button.setText("Enviando...")

        try:
            self.recovery_service.solicitar_recuperacao(email)
        except RecoveryError as exc:
            self._set_feedback(str(exc), success=False)
            return
        finally:
            self.send_button.setEnabled(True)
            self.send_button.setText("Enviar link de recuperação")

        self._set_feedback(
            "Link de recuperação enviado! Verifique seu email.", success=True
        )

    def _set_feedback(self, message, success):
        self.feedback_label.setObjectName("successLabel" if success else "errorLabel")
        self.feedback_label.style().unpolish(self.feedback_label)
        self.feedback_label.style().polish(self.feedback_label)
        self.feedback_label.setText(message)
        if not success:
            QMessageBox.warning(self, "Aviso", message)
