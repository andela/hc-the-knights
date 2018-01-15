from django.contrib.auth.hashers import make_password
from hc.test import BaseTestCase


class CheckTokenTestCase(BaseTestCase):

    def setUp(self):
        super(CheckTokenTestCase, self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()

    def test_it_shows_form(self):
        r = self.client.get("/accounts/check_token/alice/secret-token/")
        self.assertContains(r, "You are about to log in")

    def test_it_redirects(self):
        """Test method to check redirection.
        """
        r = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(r, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")

    def test_redirection_on_login(self):
        """ Test method to check if a redirection occurs
        if an existing user tries to login in.
        """
        form = {'email': self.alice.email, 'password': 'password'}
        redirect = self.client.post("/accounts/login/", form)
        self.assertRedirects(redirect, "/checks/")

    def test_invalid_token_on_login(self):
        """ Test method to check for wrong invalid token on login.
        """
        token_check = self.client.post("/accounts/check_token/alice/invalid-token/")
        self.assertRedirects(token_check, "/accounts/login/")
