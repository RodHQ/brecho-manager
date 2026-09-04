"""Conexão singleton com o MongoDB e operações de CRUD utilizadas pela app desktop."""
import threading

from pymongo import MongoClient, ReturnDocument

from utils.config import config


class MongoDBConnection:
    """Implementação singleton (thread-safe) da conexão com o MongoDB."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, uri=None, db_name=None):
        with self._lock:
            if self._initialized:
                return
            self._client = MongoClient(uri or config.MONGO_URI)
            self._db = self._client[db_name or config.MONGO_DB]
            self._initialized = True

    @property
    def db(self):
        return self._db

    @property
    def usuarios(self):
        return self._db["usuarios"]

    @property
    def recovery_tokens(self):
        return self._db["recovery_tokens"]

    def close(self):
        self._client.close()

    # --- CRUD de usuários -------------------------------------------------
    def find_usuario_by_email_ou_username(self, identifier):
        return self.usuarios.find_one(
            {"$or": [{"email": identifier}, {"username": identifier}]}
        )

    def find_usuario_by_email(self, email):
        return self.usuarios.find_one({"email": email})

    def find_usuario_by_id(self, usuario_id):
        return self.usuarios.find_one({"_id": usuario_id})

    def insert_usuario(self, usuario_doc):
        result = self.usuarios.insert_one(usuario_doc)
        return result.inserted_id

    def update_usuario_password(self, usuario_id, hashed_password):
        return self.usuarios.find_one_and_update(
            {"_id": usuario_id},
            {"$set": {"password": hashed_password}},
            return_document=ReturnDocument.AFTER,
        )

    # --- CRUD de tokens de recuperação ------------------------------------
    def insert_recovery_token(self, token_doc):
        result = self.recovery_tokens.insert_one(token_doc)
        return result.inserted_id

    def find_recovery_token(self, token):
        return self.recovery_tokens.find_one({"token": token})

    def invalidate_recovery_token(self, token):
        return self.recovery_tokens.find_one_and_update(
            {"token": token},
            {"$set": {"usado": True}},
            return_document=ReturnDocument.AFTER,
        )

    def delete_expired_recovery_tokens(self, expired_before):
        return self.recovery_tokens.delete_many({"expira_em": {"$lt": expired_before}})


def get_connection():
    """Retorna a instância singleton da conexão com o MongoDB."""
    return MongoDBConnection()
