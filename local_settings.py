'''
Configuration Settings

Includes credentials for Twilio, etc.  Second stanza intended for Heroku deployment.
'''

''' Uncomment to configure in a file.
ACCOUNT_SID = "ACxxxxxxxxxxxxx" 
AUTH_TOKEN = "yyyyyyyyyyyyyyyy"
TWILIO_APP_SID = "APzzzzzzzzz"
TWILIO_CALLER_ID = "+17778889999"
'''

# Begin Heroku configuration - configured through environment variables.
import os
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_CALLER_ID = os.environ['TWILIO_APP_SID']
TWILIO_APP_SID = os.environ['TWILIO_APP_SID']
