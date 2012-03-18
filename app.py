from flask import Flask
from twilio import twiml
import local_settings


# Declare and configure application
app = Flask(__name__, static_url_path='/static')
app.config['TWILIO_ACCOUNT_SID'] = local_settings.TWILIO_ACCOUNT_SID
app.config['TWILIO_AUTH_TOKEN'] = local_settings.TWILIO_AUTH_TOKEN
app.config['TWILIO_APP_SID'] = local_settings.TWILIO_APP_SID
app.config['TWILIO_CALLER_ID'] = local_settings.TWILIO_CALLER_ID


@app.route('/voice', methods=['POST'])
def voice():
    response = twiml.Response()
    response.say("Congratulations! You deployed the Twilio Hackpack" \
            " for Heroku and Flask.")
    return str(response)


@app.route('/sms', methods=['POST'])
def sms():
    response = twiml.Response()
    response.sms("Congratulation! You deployed the Twilio Hackpack" \
            " for Heroku and Flask.")
    return str(response)


# Run dev server if PORT not specified in environment.
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))

    if port == 5000:
        app.debug = True

    app.run(host='0.0.0.0', port=port)
