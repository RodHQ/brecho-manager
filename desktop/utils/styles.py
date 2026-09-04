"""Estilos (QSS) globais para a aplicação desktop, inspirados em Material Design."""

PRIMARY_COLOR = "#6200EE"
PRIMARY_VARIANT = "#3700B3"
ERROR_COLOR = "#B00020"
SUCCESS_COLOR = "#2E7D32"
BACKGROUND_LIGHT = "#FFFFFF"
BACKGROUND_DARK = "#121212"
SURFACE_DARK = "#1E1E1E"
TEXT_LIGHT = "#212121"
TEXT_DARK = "#FFFFFF"

LIGHT_THEME = f"""
QWidget {{
    background-color: {BACKGROUND_LIGHT};
    color: {TEXT_LIGHT};
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
}}

QLineEdit {{
    border: 1px solid #BDBDBD;
    border-radius: 6px;
    padding: 8px;
    background-color: #FAFAFA;
}}

QLineEdit:focus {{
    border: 2px solid {PRIMARY_COLOR};
}}

QPushButton {{
    background-color: {PRIMARY_COLOR};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 16px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: {PRIMARY_VARIANT};
}}

QPushButton:disabled {{
    background-color: #BDBDBD;
}}

QPushButton#linkButton {{
    background-color: transparent;
    color: {PRIMARY_COLOR};
    font-weight: normal;
    text-decoration: underline;
}}

QPushButton#linkButton:hover {{
    color: {PRIMARY_VARIANT};
}}

QLabel#errorLabel {{
    color: {ERROR_COLOR};
}}

QLabel#successLabel {{
    color: {SUCCESS_COLOR};
}}
"""

DARK_THEME = f"""
QWidget {{
    background-color: {BACKGROUND_DARK};
    color: {TEXT_DARK};
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
}}

QLineEdit {{
    border: 1px solid #424242;
    border-radius: 6px;
    padding: 8px;
    background-color: {SURFACE_DARK};
    color: {TEXT_DARK};
}}

QLineEdit:focus {{
    border: 2px solid {PRIMARY_COLOR};
}}

QPushButton {{
    background-color: {PRIMARY_COLOR};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 16px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: {PRIMARY_VARIANT};
}}

QPushButton:disabled {{
    background-color: #424242;
}}

QPushButton#linkButton {{
    background-color: transparent;
    color: #BB86FC;
    font-weight: normal;
    text-decoration: underline;
}}

QPushButton#linkButton:hover {{
    color: {PRIMARY_COLOR};
}}

QLabel#errorLabel {{
    color: #CF6679;
}}

QLabel#successLabel {{
    color: #81C784;
}}
"""


def get_theme(dark_mode=False):
    """Retorna o QSS correspondente ao tema solicitado."""
    return DARK_THEME if dark_mode else LIGHT_THEME
