from hc.api.models import Check
from hc.test import BaseTestCase
from django.contrib.auth.models import User


class AddCheckTestCase(BaseTestCase):

    def test_it_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertRedirects(r, "/checks/")
        assert Check.objects.count() == 1

    ### Test that team access works


    def test_team_access_works(self):
        alice = User.objects.get(email="alice@example.org")
        alice_bchecks = Check.objects.filter(user=alice).count()
        url = "/checks/add/"
        self.client.login(username="bob@example.org", password="password")
        self.client.post(url)
        self.client.logout()
        alice_achecks = Check.objects.filter(user=alice).count()
        self.assertEqual(alice_achecks, (alice_bchecks + 1))