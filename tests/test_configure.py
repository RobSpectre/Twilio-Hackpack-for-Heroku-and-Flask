import unittest
from mock import patch

from twilio.rest import TwilioRestClient

from .context import configure


class ConfigureTest(unittest.TestCase):
    def setUp(self):
        self.configure = configure.Configure(
                account_sid="ACxxxxx",
                auth_token="yyyyyyyy",
                phone_number="+15555555555",
                app_sid="APzzzzzzzzz")
        self.configure.client = TwilioRestClient(self.configure.account_sid,
                self.configure.auth_token)


class TwilioTest(ConfigureTest):
    @patch('twilio.rest.resources.Applications')
    @patch('twilio.rest.resources.Application')
    def test_createNewTwiMLApp(self, MockApp, MockApps):
        # Mock the Applications resource and its create method.
        self.configure.client.applications = MockApps.return_value
        self.configure.client.applications.create.return_value = \
            MockApp.return_value

        # Mock our input.
        configure.raw_input = lambda _: 'y'

        # Test
        self.configure.createNewTwiMLApp(self.configure.voice_url,
                self.configure.sms_url)

        # Assert
        self.configure.client.applications.create.assert_called_once_with(
                voice_url=self.configure.voice_url,
                sms_url=self.configure.sms_url)

    @patch('twilio.rest.resources.Applications')
    @patch('twilio.rest.resources.Application')
    def test_createNewTwiMLAppNegativeInput(self, MockApp, MockApps):
        # Mock the Applications resource and its create method.
        self.configure.client.applications = MockApps.return_value
        self.configure.client.applications.create.return_value = \
            MockApp.return_value

        # Mock our input .
        configure.raw_input = lambda _: 'n'

        # Test / Assert
        self.assertRaises(configure.ConfigurationError,
                self.configure.createNewTwiMLApp,
                self.configure.voice_url, self.configure.sms_url)

    @patch('twilio.rest.resources.Applications')
    @patch('twilio.rest.resources.Application')
    def test_setAppSidRequestUrls(self, MockApp, MockApps):
        # Mock the Applications resource and its update method.
        self.configure.client.applications = MockApps.return_value
        self.configure.client.applications.update.return_value = \
            MockApp.return_value

        # Test
        self.configure.setAppRequestUrls(self.configure.app_sid,
                self.configure.voice_url,
                self.configure.sms_url)

        # Assert
        self.configure.client.applications.update.assert_called_once_with(
                self.configure.app_sid,
                voice_url=self.configure.voice_url,
                sms_url=self.configure.sms_url,
                friendly_name='Hackpack for Heroku and Flask')

    @patch('twilio.rest.resources.PhoneNumbers')
    @patch('twilio.rest.resources.PhoneNumber')
    def test_retrievePhoneNumber(self, MockPhoneNumber, MockPhoneNumbers):
        # Mock the PhoneNumbers resource and its list method.
        mock_phone_number = MockPhoneNumber.return_value
        mock_phone_number.phone_number = self.configure.phone_number
        self.configure.client.phone_numbers = MockPhoneNumbers.return_value
        self.configure.client.phone_numbers.list.return_value = \
                [mock_phone_number]

        # Test
        self.configure.retrievePhoneNumber(self.configure.phone_number)

        # Assert
        self.configure.client.phone_numbers.list.assert_called_once_with(
                phone_number=self.configure.phone_number)

    @patch('twilio.rest.resources.PhoneNumbers')
    @patch('twilio.rest.resources.PhoneNumber')
    def test_purchasePhoneNumber(self, MockPhoneNumber, MockPhoneNumbers):
        # Mock the PhoneNumbers resource and its search and purchase methods
        mock_phone_number = MockPhoneNumber.return_value
        mock_phone_number.phone_number = self.configure.phone_number
        self.configure.client.phone_numbers = MockPhoneNumbers.return_value
        self.configure.client.phone_numbers.search = \
                [mock_phone_number]
        self.configure.client.phone_numbers.purchase = \
                mock_phone_number

        # Mock our input.
        configure.raw_input = lambda _: 'y'

        # Test
        self.configure.purchasePhoneNumber()

        # Assert
        self.configure.client.phone_numbers.purchase.assert_called_once_with()

    @patch('twilio.rest.resources.PhoneNumbers')
    @patch('twilio.rest.resources.PhoneNumber')
    def test_purchasePhoneNumberNegativeInput(self, MockPhoneNumbers,
            MockPhoneNumber):
        # Mock the PhoneNumbers resource and its search and purchase methods
        mock_phone_number = MockPhoneNumber.return_value
        mock_phone_number.phone_number = self.configure.phone_number
        self.configure.client.phone_numbers = MockPhoneNumbers.return_value
        self.configure.client.phone_numbers.search = \
                [mock_phone_number]
        self.configure.client.phone_numbers.purchase = \
                mock_phone_number

        # Mock our input.
        configure.raw_input = lambda _: 'n'

        # Test / Assert
        self.assertRaises(configure.ConfigurationError,
                self.configure.purchasePhoneNumber)

    @patch('twilio.rest.resources.Applications')
    @patch('twilio.rest.resources.Application')
    @patch('twilio.rest.resources.PhoneNumbers')
    @patch('twilio.rest.resources.PhoneNumber')
    def test_configure(self, MockPhoneNumber, MockPhoneNumbers, MockApp,
            MockApps):
        # Mock the Applications resource and its update method.
        mock_app = MockApp.return_value
        mock_app.sid = self.configure.app_sid
        self.configure.client.applications = MockApps.return_value
        self.configure.client.applications.update.return_value = \
            mock_app

        # Mock the PhoneNumbers resource and its list method.
        mock_phone_number = MockPhoneNumber.return_value
        mock_phone_number.sid = "PN123"
        mock_phone_number.friendly_name = "(555) 555-5555"
        mock_phone_number.phone_number = self.configure.phone_number
        self.configure.client.phone_numbers = MockPhoneNumbers.return_value
        self.configure.client.phone_numbers.list.return_value = \
            [mock_phone_number]

        # Test
        self.configure.configureHackpack(self.configure.voice_url,
                self.configure.sms_url,
                self.configure.app_sid,
                self.configure.phone_number)

        # Assert
        self.configure.client.applications.update.assert_called_once_with(
                self.configure.app_sid,
                voice_url=self.configure.voice_url,
                sms_url=self.configure.sms_url,
                friendly_name='Hackpack for Heroku and Flask')

        self.configure.client.phone_numbers.update.assert_called_once_with(
                "PN123",
                voice_application_sid=self.configure.app_sid,
                sms_application_sid=self.configure.app_sid,
                friendly_name='Hackpack for Heroku and Flask')

    @patch('twilio.rest.resources.Applications')
    @patch('twilio.rest.resources.Application')
    @patch('twilio.rest.resources.PhoneNumbers')
    @patch('twilio.rest.resources.PhoneNumber')
    def test_configureNoApp(self, MockPhoneNumber, MockPhoneNumbers, MockApp,
            MockApps):
        # Mock the Applications resource and its update method.
        mock_app = MockApp.return_value
        mock_app.sid = self.configure.app_sid
        self.configure.client.applications = MockApps.return_value
        self.configure.client.applications.create.return_value = \
            mock_app

        # Mock the PhoneNumbers resource and its list method.
        mock_phone_number = MockPhoneNumber.return_value
        mock_phone_number.sid = "PN123"
        mock_phone_number.friendly_name = "(555) 555-5555"
        mock_phone_number.phone_number = self.configure.phone_number
        self.configure.client.phone_numbers = MockPhoneNumbers.return_value
        self.configure.client.phone_numbers.list.return_value = \
            [mock_phone_number]

        # Set AppSid to None
        self.configure.app_sid = None

        # Mock our input.
        configure.raw_input = lambda _: 'y'

        # Test
        self.configure.configureHackpack(self.configure.voice_url,
                self.configure.sms_url,
                self.configure.app_sid,
                self.configure.phone_number)

        # Assert
        self.configure.client.applications.create.assert_called_once_with(
                voice_url=self.configure.voice_url,
                sms_url=self.configure.sms_url)

        self.configure.client.phone_numbers.update.assert_called_once_with(
                "PN123",
                voice_application_sid=mock_app.sid,
                sms_application_sid=mock_app.sid,
                friendly_name='Hackpack for Heroku and Flask')

    @patch('twilio.rest.resources.Applications')
    @patch('twilio.rest.resources.Application')
    @patch('twilio.rest.resources.PhoneNumbers')
    @patch('twilio.rest.resources.PhoneNumber')
    def test_configureNoPhoneNumber(self, MockPhoneNumber, MockPhoneNumbers,
            MockApp, MockApps):
        # Mock the Applications resource and its update method.
        mock_app = MockApp.return_value
        mock_app.sid = self.configure.app_sid
        self.configure.client.applications = MockApps.return_value
        self.configure.client.applications.update.return_value = \
            mock_app

        # Mock the PhoneNumbers resource and its list method.
        mock_phone_number = MockPhoneNumber.return_value
        mock_phone_number.sid = "PN123"
        mock_phone_number.friendly_name = "(555) 555-5555"
        mock_phone_number.phone_number = self.configure.phone_number
        self.configure.client.phone_numbers = MockPhoneNumbers.return_value
        self.configure.client.phone_numbers.purchase.return_value = \
            mock_phone_number

        # Set AppSid to None
        self.configure.phone_number = None

        # Mock our input.
        configure.raw_input = lambda _: 'y'

        # Test
        self.configure.configureHackpack(self.configure.voice_url,
                self.configure.sms_url,
                self.configure.app_sid,
                self.configure.phone_number)

        # Assert
        self.configure.client.applications.update.assert_called_once_with(
                self.configure.app_sid,
                voice_url=self.configure.voice_url,
                sms_url=self.configure.sms_url,
                friendly_name='Hackpack for Heroku and Flask')

        self.configure.client.phone_numbers.update.assert_called_once_with(
                "PN123",
                voice_application_sid=self.configure.app_sid,
                sms_application_sid=self.configure.app_sid,
                friendly_name='Hackpack for Heroku and Flask')


class HerokuTest(ConfigureTest):
    def test_getHerokuHostname(self):
        test = self.configure.getHerokuHostname(
                git_config_path='./tests/test_assets/good_git_config')
        self.assertEquals(test, 'http://look-here-snacky-11211.herokuapps.com')

    def test_getHerokuHostnameNoSuchFile(self):
        self.assertRaises(configure.ConfigurationError,
                self.configure.getHerokuHostname,
                git_config_path='/tmp')

    def test_getHerokuHostnameNoHerokuRemote(self):
        self.assertRaises(configure.ConfigurationError,
                self.configure.getHerokuHostname,
                git_config_path='./tests/test_assets/bad_git_config')


class MiscellaneousTest(unittest.TestCase):
    def test_instantiateWithoutAccountCredentials(self):
        test = configure.Configure(account_sid=None, auth_token=None,
                phone_number=None, app_sid=None)
        self.assertRaises(configure.ConfigurationError,
                test.start)
