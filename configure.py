'''
Hackpack Configure
A script to configure your TwiML apps and Twilio phone numbers to use your
hackpack's Heroku app.

Usage:

Auto-configure using your local_settings.py:
    python configure.py

Deploy to new Twilio number and App Sid:
    python configure.py --new

Deploy to specific App Sid:
    python configure.py --app APxxxxxxxxxxxxxx

Deploy to specific Twilio number:
    python configure.py --number +15556667777

Deploy to custom domain:
    python configure.py --domain example.com
'''

from optparse import OptionParser
import logging

from twilio.rest import TwilioRestClient

import local_settings

class Configure(object):
    def __init__(self, account_sid=local_settings.ACCOUNT_SID,
            auth_token=local_settings.AUTH_TOKEN,
            app_sid=local_settings.TWILIO_APP_SID,
            phone_number=local_settings.TWILIO_CALLER_ID,
            voice_endpoint=None,
            sms_endpoint=None,
            domain=None):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.app_sid = app_sid
        self.phone_number = phone_number
        self.domain = domain
        self.voice_endpoint = voice_endpoint
        self.sms_endpoint = sms_endpoint
        self.client = TwilioRestClient(account_sid, auth_token)

    def setVoiceEndpoint():




# Logging configuration
logging_level = logging.INFO
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setLevel(logging_level)
log_formatter = logging.Formatter('%(asctime)s::%(name)s::' \
        '%(levelname)s::%(message)s')
log_handler.setFormatter(log_formatter)


# Parser configuration
usage = "usage: %prog [options] arg1 arg2"
parser = OptionParser(usage=usage)
parser.add_option("-n", "--new", default=False,
        help="Purchase new Twilio phone number and configure app to use" \
            "hackpack.")
parser.add_option("-a", "--app", default=None,
        help="Configure specific AppSid to use hackpack endpoints.")
parser.add_option("-#", "--number", default=None,
        help="Configure specific Twilio number to use hackpack endpoints.")
parser.add_option("-v", "--voice", default='/voice',
        help="Set the route for your Voice Request URL: (e.g. '/voice').")
parser.add_option("-s", "--sms", default='/sms',
        help="Set the route for your SMS Request URL: (e.g. '/sms').")
parser.add_option("-d", "--domain", default=None,
        help="Set a custom domain.")
parser.add_option("-V", "--verbose", default=None,
        help="Turn on verbose output.")
parser.add_option("-D", "--debug", default=None,
        help="Turn on debug output.")


def main():
    (options, args) = parser.parse_args()


if __name__ == "__main__":
    main()
