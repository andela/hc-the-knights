from hc.api.models import Check
from hc.test import BaseTestCase
from datetime import timedelta as td

from django.utils import timezone

class UnresolvedchecksTestCase(BaseTestCase):

    def setUp(self):
        super(UnresolvedchecksTestCase, self).setUp()
        self.check = Check(user=self.alice, name="I failed to work")
        self.check.last_ping = timezone.now() - td(days=3)
        self.check.status = "down"
        self.check.save()

    def test_it_works(self):

        for email in ("alice@example.org", "bob@example.org"):
            self.client.login(username=email, password="password")
            result = self.client.get("/checks/unresolved")
            self.assertContains(result, "I failed to work", status_code=200)