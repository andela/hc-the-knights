import json
from datetime import timedelta as td
from django.utils.timezone import now

from hc.api.models import Check
from hc.test import BaseTestCase


class ListChecksTestCase(BaseTestCase):
    URL = "/api/v1/checks/"

    def setUp(self):
        super(ListChecksTestCase, self).setUp()

        self.now = now().replace(microsecond=0)

        self.a1 = Check(user=self.alice, name="Alice 1")
        self.a1.timeout = td(seconds=3600)
        self.a1.grace = td(seconds=900)
        self.a1.last_ping = self.now
        self.a1.n_pings = 1
        self.a1.status = "new"
        self.a1.save()

        self.a2 = Check(user=self.alice, name="Alice 2")
        self.a2.timeout = td(seconds=86400)
        self.a2.grace = td(seconds=3600)
        self.a2.last_ping = self.now
        self.a2.status = "up"
        self.a2.save()

    def get(self):
        return self.client.get("/api/v1/checks/", HTTP_X_API_KEY="abc")

    def test_it_works(self):
        r = self.get()
        # Assert the response status code
        self.assertEqual(r.status_code, 200)
        doc = r.json()
        self.assertTrue("checks" in doc)

        checks = {check["name"]: check for check in doc["checks"]}

        # Assert the expected length of checks
        # Assert the checks Alice 1 and Alice 2's timeout, grace, ping_url, status,
        # last_ping, n_pings and pause_url
        ping_endpoint = 'http://localhost:8000/ping/'
        alice_2_code = str(self.a2.code)
        alice_2_ping_url = ping_endpoint + alice_2_code
        pauseurl = '/api/v1/checks/'
        alice_2_pause_url = ping_endpoint + pauseurl + alice_2_code

        # Alice 1 tests
        self.assertTrue(0 < len(checks['Alice 1']['name']) <= 100)
        self.assertEqual(checks['Alice 1']['timeout'], 3600)
        self.assertEqual(checks['Alice 1']['grace'], 900)
        self.assertTrue(alice_2_ping_url)
        self.assertEqual(checks['Alice 1']['status'], self.a1.status)
        self.assertTrue(checks['Alice 1']['pause_url'])
        self.assertTrue(checks['Alice 1']['n_pings'], self.a1.n_pings)
        self.assertTrue(checks['Alice 1']['last_ping'],
                        self.a1.to_dict()['last_ping'])

        # Alice 2 tests
        self.assertTrue(0 < len(checks['Alice 2']['name']) <= 100)
        self.assertEqual(checks['Alice 2']['timeout'], 86400)
        self.assertEqual(checks['Alice 2']['grace'], 3600)
        self.assertTrue(alice_2_ping_url)
        self.assertEqual(checks['Alice 2']['status'], self.a2.status)
        self.assertTrue(checks['Alice 2']['pause_url'])
        self.assertEqual(checks['Alice 2']['n_pings'], self.a2.n_pings)
        self.assertEqual(checks['Alice 2']['last_ping'],
                         self.a2.to_dict()['last_ping'])

    def test_it_shows_only_users_checks(self):
        bobs_check = Check(user=self.bob, name="Bob 1")
        bobs_check.save()
        r = self.get()
        data = r.json()
        self.assertEqual(len(data["checks"]), 2)
        for check in data["checks"]:
            self.assertNotEqual(check["name"], "Bob 1")

    # Test that it accepts an api_key in the request
    def test_it_accepts_api_key(self):

        r = self.client.generic('GET', self.URL, json.dumps({"api_key": "abc"}),
                                content_type="application/json")
        self.assertEqual(r.status_code, 200)
