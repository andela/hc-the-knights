from hc.test import BaseTestCase
from hc.api.models import Check
from django.contrib.auth.models import User


class SwitchTeamTestCase(BaseTestCase):

    def test_it_switches(self):
        b = User.objects.get(email="bob@example.org")
        c = Check(user=self.alice, name="This belongs to Alice", member_allowed_access=True, member_allowed_id=b.id)
        c.save()

        self.client.login(username="bob@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        r = self.client.get(url, follow=True)
        # Assert the contents of r
        self.assertContains(r, c.name)

    def test_it_checks_team_membership(self):
        self.client.login(username="charlie@example.org", password="password")
        url = "/accounts/switch_team/%s/" % self.alice.username
        r = self.client.get(url)
        # Assert the expected error code
        self.assertEqual(r.status_code, 403)

    def test_it_switches_to_own_team(self):
        self.client.login(username="alice@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        r = self.client.get(url, follow=True)
        # Assert the expected error code
        self.assertEqual(r.status_code, 200)
