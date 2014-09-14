import unittest
from .context import app

app.config['TWILIO_ACCOUNT_SID'] = 'ACxxxxxx'
app.config['TWILIO_AUTH_TOKEN'] = 'yyyyyyyyy'
app.config['TWILIO_CALLER_ID'] = '+15558675309'
app.config['TWILIO_APP_SID'] = 'APzzzzzzzzzzzz'


class WebTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()


class ExampleTests(WebTest):
    def test_index(self):
        response = self.app.get('/')
        self.assertEqual("200 OK", response.status)

    def test_client(self):
        response = self.app.get('/client')
        self.assertEqual("200 OK", response.status)

    def test_client_no_app_config(self):
        app.config['TWILIO_ACCOUNT_SID'] = None
        response = self.app.get('/client')
        self.assertEqual("200 OK", response.status)
        self.assertTrue(b"Missing from local_settings" in response.data,
                        "Could not find missing config message in response.")

    def test_client_incoming(self):
        response = self.app.post('/client/incoming',
                                 data={'PhoneNumber': '16667778888'})
        self.assertEqual("200 OK", response.status)
        self.assertTrue(b"</Dial>" in response.data, "Could not find <Dial>"
                        "in response: {0}".format(response.data))
        self.assertTrue(b'16667778888' in response.data, "Could not find "
                        "inputted phone number: {0}".format(response.data))

    def test_client_incoming_no_phone_number(self):
        response = self.app.post('/client/incoming')
        self.assertEqual("200 OK", response.status)
        self.assertFalse(b"<Dial>" in response.data, "Found <Dial>"
                         "in response when should have returned "
                         "error: {0}".format(response.data))
        self.assertFalse(b'16667778888' in response.data, "Found "
                         "inputted phone number when should have returned "
                         "error: {0}".format(response.data))
        self.assertTrue(b'<Say>' in response.data, "Did not find "
                        "error message in response: {0}".format(response.data))

    def test_client_incoming_no_caller_id(self):
        app.config.pop("TWILIO_CALLER_ID", None)
        response = self.app.post('/client/incoming',
                                 data={'PhoneNumber': '16667778888'})
        self.assertEqual("200 OK", response.status)
        self.assertFalse(b"<Dial>" in response.data, "Found <Dial>"
                         "in response when should have returned "
                         "error: {0}".format(response.data))
        self.assertFalse(b'16667778888' in response.data, "Found "
                         "inputted phone number when should have returned "
                         "error: {0}".format(response.data))
        self.assertTrue(b'<Say>' in response.data, "Did not find "
                        "error message in response: {0}".format(response.data))

    def test_client_incoming_incorrect_number(self):
        response = self.app.post('/client/incoming',
                                 data={'PhoneNumber': 'AKJD:LFKNAFJ'})
        self.assertEqual("200 OK", response.status)
        self.assertFalse(b"<Dial>" in response.data, "Found <Dial>"
                         "in response when should have returned "
                         "error: {0}".format(response.data))
        self.assertFalse(b'16667778888' in response.data, "Found "
                         "inputted phone number when should have returned "
                         "error: {0}".format(response.data))
        self.assertTrue(b'<Say>' in response.data, "Did not find "
                        "error message in response: {0}".format(response.data))
