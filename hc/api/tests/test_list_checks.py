import json
from datetime import timedelta as td
from django.utils.timezone import now

from hc.api.models import Check
from hc.test import BaseTestCase


class ListChecksTestCase(BaseTestCase):

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
        # print('check name', check['name'])
        print('\n')
        print('checks:', checks)
        print('alice:', checks['Alice 2'])
        alice_2 = checks['Alice 2']
        print('alice name:', alice_2['name'])
        alice_2_name = alice_2['name']
        alice_2_timeout = alice_2['timeout']
        alice_2_grace = alice_2['grace']
        ping_endpoint = 'http://localhost:8000/ping/'
        alice_2_code = str(self.a2.code)
        alice_2_ping_url = ping_endpoint + alice_2_code
        alice_2_status = alice_2['status']
        pauseurl = '/api/v1/checks/'
        alice_2_pause_url = ping_endpoint + pauseurl + alice_2_code
        for check in checks:
            print('checks', check)
        # Assert the expected length of checks
        # Assert the checks Alice 1 and Alice 2's timeout, grace, ping_url, status,
        ### last_ping, n_pings and pause_url

        self.assertTrue(0 < len(alice_2_name) <= 100)
        self.assertEqual(alice_2_timeout, 86400)
        self.assertTrue(alice_2_grace, 3600)
        self.assertTrue(alice_2_ping_url)
        self.assertEqual(alice_2_status, 'up')
        self.assertTrue(alice_2_pause_url)

    def test_it_shows_only_users_checks(self):
        bobs_check = Check(user=self.bob, name="Bob 1")
        bobs_check.save()

        r = self.get()
        data = r.json()
        self.assertEqual(len(data["checks"]), 2)
        for check in data["checks"]:
            self.assertNotEqual(check["name"], "Bob 1")

    # Test that it accepts an api_key in the request
