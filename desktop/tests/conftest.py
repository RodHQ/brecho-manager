"""Configuração do pytest para os testes da aplicação desktop."""
import os
import sys

DESKTOP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if DESKTOP_DIR not in sys.path:
    sys.path.insert(0, DESKTOP_DIR)
