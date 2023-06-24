from django.urls import reverse

from opentoilet.tests import BaseTest


class LoginTestCase(BaseTest):
    url = reverse("accounts-login")

    def test_login_with_valid_credentials(self):
        data = {"username": self.username, "password": self.password}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)

    def test_login_with_invalid_credentials(self):
        data = {"username": "invaliduser", "password": "invalidpass"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("invalid_credentials", response.data["code"])

    def test_login_with_incomplete_account(self):
        self.user.account.setup_complete = False
        self.user.account.save()
        data = {"username": self.username, "password": self.password}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("account_incomplete", response.data["code"])
