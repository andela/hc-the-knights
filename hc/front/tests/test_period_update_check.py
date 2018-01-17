from hc.api.models import Check
from hc.test import BaseTestCase


class PeriodTimeoutTestcase(BaseTestCase):

    def setUp(self):
        super(PeriodTimeoutTestcase, self).setUp()
        self.check = Check(user=self.alice)
        self.check.save()

    def test_timeout_over_one_month(self):
        url = "/checks/%s/timeout/" % self.check.code
        payload = {"timeout": 5184000, "grace": 5100000}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, data=payload)
        self.assertRedirects(r, "/checks/")

        check = Check.objects.get(code=self.check.code)
        assert check.timeout.total_seconds() == 5184000
        assert check.grace.total_seconds() == 5100000