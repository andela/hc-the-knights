from hc.api.models import Check
from hc.test import BaseTestCase
from datetime import timedelta as td
from django.utils import timezone


class MyChecksTestCase(BaseTestCase):

    def setUp(self):
        super(MyChecksTestCase, self).setUp()
        self.check = Check(user=self.alice)
        self.check.save()

    def test_it_works(self):
        url = "/checks/%s/name/" % self.check.code
        url_2 = "/checks/department=marketing?"
        payload = {"name": "Alice check", "department": "marketing"}
        
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, data=payload)
        self.assertRedirects(r, "/checks/")
        h = self.client.get(url_2)
        self.assertContains(h, "Alice check")
        