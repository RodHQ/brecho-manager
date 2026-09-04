"""Tela principal/dashboard exibida após o login."""
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from utils.config import config
from utils.styles import get_theme


class MainWindow(QWidget):
    """Janela principal exibida após a autenticação bem-sucedida."""

    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.login_window = None
        self._build_ui()

    def _build_ui(self):
        self.setWindowTitle(f"{config.APP_NAME} - Dashboard")
        self.setMinimumSize(480, 320)
        self.setStyleSheet(get_theme(dark_mode=False))

        layout = QVBoxLayout()
        layout.setSpacing(12)

        welcome_label = QLabel(f"Bem-vindo(a), {self.usuario.nome_exibicao}!")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(welcome_label)

        placeholder_label = QLabel(
            "Espaço reservado para os módulos: clientes, estoque, "
            "transações e fornecedores."
        )
        placeholder_label.setWordWrap(True)
        layout.addWidget(placeholder_label)

        layout.addStretch()

        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.handle_logout)
        layout.addWidget(self.logout_button)

        self.setLayout(layout)

    def handle_logout(self):
        """Remove o token de sessão local e reabre a tela de login."""
        from ui.login_window import LoginWindow

        if os.path.exists(".token"):
            try:
                os.remove(".token")
            except OSError:
                pass

        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
