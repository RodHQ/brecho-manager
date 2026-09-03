from django.test import SimpleTestCase


class ProjectConfigurationTests(SimpleTestCase):
    def test_homepage_is_available(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
