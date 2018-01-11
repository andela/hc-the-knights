import json

from hc.api.models import Channel, Check
from hc.test import BaseTestCase


class CreateCheckTestCase(BaseTestCase):
    URL = "/api/v1/checks/"

    def setUp(self):
        super(CreateCheckTestCase, self).setUp()

    def post(self, data, expected_error=None):
        r = self.client.post(self.URL, json.dumps(data),
                             content_type="application/json")

        if expected_error:
            self.assertEqual(r.status_code, 400)
            ### Assert that the expected error is the response error
            result = r.json()
            self.assertEqual(result['error'], expected_error)

        return r

    def test_it_works(self):
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60
        })

        self.assertEqual(r.status_code, 201)

        doc = r.json()
        assert "ping_url" in doc
        self.assertEqual(doc["name"], "Foo")
        self.assertEqual(doc["tags"], "bar,baz")

        ### Assert the expected last_ping and n_pings values
        self.assertEqual(doc["last_ping"], None)
        self.assertEqual(doc["n_pings"], 0)

        self.assertEqual(Check.objects.count(), 1)
        check = Check.objects.get()
        self.assertEqual(check.name, "Foo")
        self.assertEqual(check.tags, "bar,baz")
        self.assertEqual(check.timeout.total_seconds(), 3600)
        self.assertEqual(check.grace.total_seconds(), 60)

    def test_it_accepts_api_key_in_header(self):
        payload = json.dumps({"name": "Foo"})

        ### Make the post request and get the response
        r = {'status_code': 201} ### This is just a placeholder variable
        response = self.client.post(self.URL, payload, content_type="application/json", HTTP_X_API_KEY="abc")

        self.assertEqual(response.status_code, 201)

    def test_it_handles_missing_request_body(self):
        ### Make the post request with a missing body and get the response
        r = {'status_code': 400, 'error': "wrong api_key"} ### This is just a placeholder variable

        data = json.dumps({})
        response = self.client.post(self.URL, data, content_type="application/json")
        
        self.assertEqual(response.status_code, 400)

    def test_it_handles_invalid_json(self):
        ### Make the post request with invalid json data type
        r = {'status_code': 400, 'error': "could not parse request body"} ### This is just a placeholder variable
        data = {"name": "Foo", "tags": "bar,baz"}
        response = self.client.post(self.URL, data, content_type="application/json", HTTP_X_API_KEY="abc")
        r = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(r["error"], "could not parse request body")

    def test_it_rejects_wrong_api_key(self):
        self.post({"api_key": "wrong"},
                  expected_error="wrong api_key")

    def test_it_rejects_non_number_timeout(self):
        self.post({"api_key": "abc", "timeout": "oops"},
                  expected_error="timeout is not a number")
        
    def test_it_rejects_non_string_name(self):
        self.post({"api_key": "abc", "name": False},
                  expected_error="name is not a string")

    ### Test for the assignment of channels
    def test_it_assigns_channels(self):
        channel = Channel(user=self.alice)
        channel.save()

        response = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60
        })
        check = Check.objects.get(user=self.alice, name="Foo")
        check.assign_all_channels()

        self.assertEqual(check.channel_set.count(), 1)

    ### Test for the 'timeout is too small' and 'timeout is too large' errors
    def test_too_small_time_outs(self):
        self.post(
            {
                "api_key": "abc",
                "name": 'twiter',
                "timeout": 0
            },
            expected_error="timeout is too small")

    def test_too_large_time_outs(self):
        self.post(
            {
                "api_key": "abc",
                "name": 'Some name',
                "timeout": 1000000000
            },
            expected_error="timeout is too large")
