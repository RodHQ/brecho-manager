"""Utilitários para testes que usam MongoEngine com um MongoDB em memória (mongomock)."""

import mongoengine
import mongomock
from django.test import SimpleTestCase


class MongoTestCase(SimpleTestCase):
    """TestCase que conecta o MongoEngine a um MongoDB em memória (mongomock).

    Evita a necessidade de uma instância real do MongoDB durante os testes.
    """

    databases = []
    mongo_alias = "default"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        mongoengine.disconnect(alias=cls.mongo_alias)
        mongoengine.connect(
            "mongoenginetest",
            host="localhost",
            mongo_client_class=mongomock.MongoClient,
            alias=cls.mongo_alias,
        )

    @classmethod
    def tearDownClass(cls):
        mongoengine.disconnect(alias=cls.mongo_alias)
        super().tearDownClass()
