"""Tela de login desktop (PyQt6)."""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from services.auth_service import AuthError, AuthService
from ui.main_window import MainWindow
from ui.recovery_dialog import RecoveryDialog
from utils.config import config
from utils.styles import get_theme
from utils.validators import is_not_empty


class LoginWindow(QWidget):
    """Janela de login com email/usuário, senha e link de recuperação."""

    def __init__(self, auth_service=None):
        super().__init__()
        self.auth_service = auth_service or AuthService()
        self.main_window = None
        self._build_ui()

    def _build_ui(self):
        self.setWindowTitle(f"{config.APP_NAME} - Login")
        self.setMinimumWidth(360)
        self.setStyleSheet(get_theme(dark_mode=False))

        layout = QVBoxLayout()
        layout.setSpacing(12)

        title = QLabel(config.APP_NAME)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        self.identifier_input = QLineEdit()
        self.identifier_input.setPlaceholderText("Email ou usuário")
        layout.addWidget(self.identifier_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.feedback_label = QLabel("")
        self.feedback_label.setObjectName("errorLabel")
        self.feedback_label.setWordWrap(True)
        layout.addWidget(self.feedback_label)

        self.login_button = QPushButton("Entrar")
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.forgot_password_button = QPushButton("Esqueci minha senha")
        self.forgot_password_button.setObjectName("linkButton")
        self.forgot_password_button.clicked.connect(self.open_recovery_dialog)
        layout.addWidget(self.forgot_password_button)

        self.setLayout(layout)

    def handle_login(self):
        identifier = self.identifier_input.text().strip()
        password = self.password_input.text()

        if not is_not_empty(identifier) or not is_not_empty(password):
            self._show_feedback("Preencha usuário/email e senha.", success=False)
            return

        try:
            usuario, token = self.auth_service.login(identifier, password)
        except AuthError as exc:
            self._show_feedback(str(exc), success=False)
            return

        self._salvar_token(token)
        self._show_feedback("Login realizado com sucesso!", success=True)
        self._abrir_dashboard(usuario)

    def _salvar_token(self, token):
        """Armazena o token JWT em arquivo local para manter a sessão."""
        try:
            with open(".token", "w", encoding="utf-8") as arquivo:
                arquivo.write(token)
        except OSError:
            pass

    def _abrir_dashboard(self, usuario):
        self.main_window = MainWindow(usuario)
        self.main_window.show()
        self.close()

    def open_recovery_dialog(self):
        dialog = RecoveryDialog(self)
        dialog.exec()

    def _show_feedback(self, message, success):
        self.feedback_label.setObjectName("successLabel" if success else "errorLabel")
        self.feedback_label.style().unpolish(self.feedback_label)
        self.feedback_label.style().polish(self.feedback_label)
        self.feedback_label.setText(message)
        if not success:
            QMessageBox.warning(self, "Aviso", message)
