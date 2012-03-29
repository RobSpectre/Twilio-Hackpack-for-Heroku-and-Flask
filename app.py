import os
import signal

from flask import Flask
from flask import render_template
from flask import url_for
from flask import request

from twilio import twiml
from twilio.util import TwilioCapability

import local_settings


# Declare and configure application
app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('local_settings.py')


# Voice Request URL
@app.route('/voice', methods=['POST'])
def voice():
    response = twiml.Response()
    response.say("Congratulations! You deployed the Twilio Hackpack" \
            " for Heroku and Flask.")
    return str(response)


# SMS Request URL
@app.route('/sms', methods=['POST'])
def sms():
    response = twiml.Response()
    response.sms("Congratulation! You deployed the Twilio Hackpack" \
            " for Heroku and Flask.")
    return str(response)


# Twilio Client demo template
@app.route('/client')
def client():
    configuration_error = None
    for key in ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_APP_SID',
            'TWILIO_CALLER_ID']:
        if not app.config[key]:
            configuration_error = "Missing from local_settings.py: " \
                    "%s" % key
            token = None
    if not configuration_error:
        capability = TwilioCapability(app.config['TWILIO_ACCOUNT_SID'],
            app.config['TWILIO_AUTH_TOKEN'])
        capability.allow_client_incoming("joey_ramone")
        capability.allow_client_outgoing(app.config['TWILIO_APP_SID'])
        token = capability.generate()
    return render_template('client.html', token=token,
            configuration_error=configuration_error)


# Installation success page
@app.route('/')
def index():
    params = {
        'voice_request_url': url_for('.voice', _external=True),
        'sms_request_url': url_for('.sms', _external=True),
        'client_url': url_for('.client', _external=True)}
    return render_template('index.html', params=params)

# Handles SIGTERM so that we don't get an error when Heroku wants or needs to restart the dyno
def graceful_shutdown(signum, frame):
    exit()

signal.signal(signal.SIGTERM, graceful_shutdown)


# If PORT not specified by environment, assume development config.
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
