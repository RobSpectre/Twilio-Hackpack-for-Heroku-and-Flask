import unittest
from twilio.util import RequestValidator
from .context import app


app.config['SERVER_NAME'] = 'localhost'
app.config['TWILIO_ACCOUNT_SID'] = 'ACxxxxxx'
app.config['TWILIO_AUTH_TOKEN'] = 'yyyyyyyyy'
app.config['TWILIO_CALLER_ID'] = '+15558675309'


class TwiMLTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.validator = RequestValidator(app.config['TWILIO_AUTH_TOKEN'])

    def assertTwiML(self, response):
        self.assertTrue("<Response>" in response.data, "Did not find " \
                "<Response>: %s" % response.data)
        self.assertTrue("</Response>" in response.data, "Did not find " \
                "</Response>: %s" % response.data)
        self.assertEqual("200 OK", response.status)

    def sms(self, body, url='/sms', to=app.config['TWILIO_CALLER_ID'],
            from_='+15558675309', extra_params=None, signed=True):
        params = {
            'SmsSid': 'SMtesting',
            'AccountSid': app.config['TWILIO_ACCOUNT_SID'],
            'To': to,
            'From': from_,
            'Body': body,
            'FromCity': 'BROOKLYN',
            'FromState': 'NY',
            'FromCountry': 'US',
            'FromZip': '55555'}
        if extra_params:
            params = dict(params.items() + extra_params.items())
        if signed:
            abs_url = 'http://{0}{1}'.format(app.config['SERVER_NAME'], url)
            signature = self.validator.compute_signature(abs_url, params)
            return self.app.post(url, data=params,
                                headers={'X-Twilio-Signature': signature})
        return self.app.post(url, data=params)

    def call(self, url='/voice', to=app.config['TWILIO_CALLER_ID'],
            from_='+15558675309', digits=None, extra_params=None, signed=True):
        params = {
            'CallSid': 'CAtesting',
            'AccountSid': app.config['TWILIO_ACCOUNT_SID'],
            'To': to,
            'From': from_,
            'CallStatus': 'ringing',
            'Direction': 'inbound',
            'FromCity': 'BROOKLYN',
            'FromState': 'NY',
            'FromCountry': 'US',
            'FromZip': '55555'}
        if digits:
            params['Digits'] = digits
        if extra_params:
            params = dict(params.items() + extra_params.items())
        if signed:
            abs_url = 'http://{0}{1}'.format(app.config['SERVER_NAME'], url)
            signature = self.validator.compute_signature(abs_url, params)
            return self.app.post(url, data=params,
                                headers={'X-Twilio-Signature': signature})
        return self.app.post(url, data=params)


class ExampleTests(TwiMLTest):
    def test_sms(self):
        response = self.sms("Test")
        self.assertTwiML(response)

    def test_voice(self):
        response = self.call()
        self.assertTwiML(response)

    def test_unsigned_sms_fails(self):
        response = self.sms("Test", signed=False)
        self.assertEqual(response.status_code, 403)

    def test_unsigned_voice_fails(self):
        response = self.call(signed=False)
        self.assertEqual(response.status_code, 403)
