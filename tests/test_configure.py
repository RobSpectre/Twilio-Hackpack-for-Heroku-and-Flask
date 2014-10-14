import unittest
from mock import Mock
from mock import patch
import subprocess
import logging

from twilio.rest import TwilioRestClient
from twilio.exceptions import TwilioException

from .context import configure


class ConfigureTest(unittest.TestCase):
    def setUp(self):
        self.configure = configure.Configure(account_sid="ACxxxxx",
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
        app_create = self.configure.client.applications.create
        app_create.assert_called_once_with(voice_url=self.configure.voice_url,
                                           sms_url=self.configure.sms_url,
                                           friendly_name="Hackpack for Heroku "
                                                         "and Flask")

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
                          self.configure.voice_url,
                          self.configure.sms_url)

    @patch('twilio.rest.resources.Applications')
    def test_createNewTwiMLAppException(self, MockApps):
        # Mock the Applications resource and its create method.
        self.configure.client.applications = MockApps.return_value

        def raiseException(*args, **kwargs):
            raise TwilioException("Test error.")

        self.configure.client.applications.create.side_effect = raiseException

        # Mock our input .
        configure.raw_input = lambda _: 'y'

        # Test / Assert
        self.assertRaises(configure.ConfigurationError,
                          self.configure.createNewTwiMLApp,
                          self.configure.voice_url,
                          self.configure.sms_url)

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
        app_create = self.configure.client.applications.update
        app_create.assert_called_once_with(self.configure.app_sid,
                                           voice_url=self.configure.voice_url,
                                           sms_url=self.configure.sms_url,
                                           friendly_name='Hackpack for Heroku '
                                                         'and Flask')

    @patch('twilio.rest.resources.Applications')
    def test_setAppSidRequestUrls404Error(self, MockApps):
        # Mock the Applications resource and its update method.
        self.configure.client.applications.update = MockApps()

        def raiseException(*args, **kwargs):
            raise TwilioException("HTTP ERROR 404.")

        self.configure.client.applications.update.side_effect = raiseException

        # Test
        self.assertRaises(configure.ConfigurationError,
                          self.configure.setAppRequestUrls,
                          self.configure.app_sid,
                          self.configure.voice_url,
                          self.configure.sms_url)

    @patch('twilio.rest.resources.Applications')
    def test_setAppSidRequestUrls500Error(self, MockApps):
        # Mock the Applications resource and its update method.
        self.configure.client.applications.update = MockApps()

        def raiseException(*args, **kwargs):
            raise TwilioException("HTTP ERROR 500.")

        self.configure.client.applications.update.side_effect = raiseException

        # Test
        self.assertRaises(configure.ConfigurationError,
                          self.configure.setAppRequestUrls,
                          self.configure.app_sid,
                          self.configure.voice_url,
                          self.configure.sms_url)

    @patch('twilio.rest.resources.PhoneNumbers')
    @patch('twilio.rest.resources.PhoneNumber')
    def test_retrievePhoneNumber(self, MockPhoneNumber, MockPhoneNumbers):
        # Mock the PhoneNumbers resource and its list method.
        mock_num = MockPhoneNumber.return_value
        mock_num.phone_number = self.configure.phone_number
        self.configure.client.phone_numbers = MockPhoneNumbers.return_value
        self.configure.client.phone_numbers.list.return_value = [mock_num]

        # Test
        self.configure.retrievePhoneNumber(self.configure.phone_number)

        # Assert
        num_l = self.configure.client.phone_numbers.list
        num_l.assert_called_once_with(phone_number=self.configure.phone_number)

    @patch('twilio.rest.resources.PhoneNumbers')
    @patch('twilio.rest.resources.PhoneNumber')
    def test_purchasePhoneNumber(self, MockPhoneNumber, MockPhoneNumbers):
        # Mock the PhoneNumbers resource and its search and purchase methods
        mock_phone_number = MockPhoneNumber.return_value
        mock_phone_number.phone_number = self.configure.phone_number
        self.configure.client.phone_numbers = MockPhoneNumbers.return_value
        self.configure.client.phone_numbers.purchase = mock_phone_number

        # Mock our input.
        configure.raw_input = lambda _: 'y'

        # Test
        self.configure.purchasePhoneNumber()

        # Assert
        purchase = self.configure.client.phone_numbers.purchase
        purchase.assert_called_once_with(area_code="646")

    @patch('twilio.rest.resources.PhoneNumbers')
    @patch('twilio.rest.resources.PhoneNumber')
    def test_purchasePhoneNumberNegativeInput(self, MockPhoneNumbers,
                                              MockPhoneNumber):
        # Mock the PhoneNumbers resource and its search and purchase methods
        mock_phone_number = MockPhoneNumber.return_value
        mock_phone_number.phone_number = self.configure.phone_number
        self.configure.client.phone_numbers = MockPhoneNumbers.return_value
        self.configure.client.phone_numbers.purchase = mock_phone_number

        # Mock our input.
        configure.raw_input = lambda _: 'n'

        # Test / Assert
        self.assertRaises(configure.ConfigurationError,
                          self.configure.purchasePhoneNumber)

    @patch('twilio.rest.resources.PhoneNumbers')
    def test_purchasePhoneNumberExceptionOnPurchase(self, MockPhoneNumbers):
        # Mock the PhoneNumbers resource and its search and purchase methods
        self.configure.client.phone_numbers.purchase = MockPhoneNumbers()

        def raiseException(*args, **kwargs):
            raise TwilioException("Test error.")

        self.configure.client.phone_numbers.purchase.side_effect = \
            raiseException

        # Mock our input.
        configure.raw_input = lambda _: 'y'

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
        apps = self.configure.client.applications.update
        apps.assert_called_once_with(self.configure.app_sid,
                                     voice_url=self.configure.voice_url,
                                     sms_url=self.configure.sms_url,
                                     friendly_name='Hackpack for Heroku '
                                                   'and Flask')

        update = self.configure.client.phone_numbers.update
        app_sid = self.configure.app_sid
        update.assert_called_once_with("PN123",
                                       voice_application_sid=app_sid,
                                       sms_application_sid=app_sid)

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
        create = self.configure.client.applications.create
        create.assert_called_once_with(voice_url=self.configure.voice_url,
                                       sms_url=self.configure.sms_url,
                                       friendly_name="Hackpack for Heroku "
                                                     "and Flask")

        update = self.configure.client.phone_numbers.update
        update.assert_called_once_with("PN123",
                                       voice_application_sid=mock_app.sid,
                                       sms_application_sid=mock_app.sid)

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
        update = self.configure.client.applications.update
        update.assert_called_once_with(self.configure.app_sid,
                                       voice_url=self.configure.voice_url,
                                       sms_url=self.configure.sms_url,
                                       friendly_name='Hackpack for Heroku '
                                                     'and Flask')

        update = self.configure.client.phone_numbers.update
        app_sid = self.configure.app_sid
        update.assert_called_once_with("PN123",
                                       voice_application_sid=app_sid,
                                       sms_application_sid=app_sid)

    @patch('twilio.rest.resources.Applications')
    @patch('twilio.rest.resources.Application')
    @patch('twilio.rest.resources.PhoneNumbers')
    @patch('twilio.rest.resources.PhoneNumber')
    def test_configureNoPhoneNumberTwilioError(self, MockPhoneNumber,
                                               MockPhoneNumbers, MockApp,
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

        def raiseException(*args, **kwargs):
            raise TwilioException("Test error.")

        self.configure.client.phone_numbers.update.side_effect = \
            raiseException

        # Mock our input.
        configure.raw_input = lambda _: 'y'

        # Test
        self.assertRaises(configure.ConfigurationError,
                          self.configure.configureHackpack,
                          self.configure.voice_url,
                          self.configure.sms_url,
                          self.configure.app_sid,
                          self.configure.phone_number)

    @patch.object(subprocess, 'call')
    @patch.object(configure.Configure, 'configureHackpack')
    def test_start(self, mock_configureHackpack, mock_call):
        mock_call.return_value = None
        self.configure.host = 'http://look-here-snacky-11211.herokuapp.com'
        self.configure.start()
        m = mock_configureHackpack
        m.assert_called_once_with('http://look-here-snacky-11211.herokuapp.com'
                                  '/voice',
                                  'http://look-here-snacky-11211.herokuapp.com'
                                  '/sms',
                                  self.configure.app_sid,
                                  self.configure.phone_number)

    @patch.object(subprocess, 'call')
    @patch.object(configure.Configure, 'configureHackpack')
    @patch.object(configure.Configure, 'getHerokuHostname')
    def test_startWithoutHostname(self, mock_getHerokuHostname,
                                  mock_configureHackpack, mock_call):
        mock_call.return_value = None
        mock_getHerokuHostname.return_value = 'http://look-here-snacky-11211' \
                                              '.herokuapp.com'
        self.configure.start()
        m = mock_configureHackpack
        m.assert_called_once_with('http://look-here-snacky-11211.herokuapp.com'
                                  '/voice',
                                  'http://look-here-snacky-11211.herokuapp.com'
                                  '/sms',
                                  self.configure.app_sid,
                                  self.configure.phone_number)


class HerokuTest(ConfigureTest):
    def test_getHerokuHostname(self):
        test = self.configure.getHerokuHostname(git_config_path='./tests'
                                                                '/test_assets'
                                                                '/good_git_'
                                                                'config')
        self.assertEquals(test, 'http://look-here-snacky-11211.herokuapp.com')

    def test_getHerokuHostnameNoSuchFile(self):
        self.assertRaises(configure.ConfigurationError,
                          self.configure.getHerokuHostname,
                          git_config_path='/tmp')

    def test_getHerokuHostnameNoHerokuRemote(self):
        self.assertRaises(configure.ConfigurationError,
                          self.configure.getHerokuHostname,
                          git_config_path='./tests/test_assets/bad_git_config')

    @patch.object(subprocess, 'call')
    def test_setHerokuEnvironmentVariables(self, mock_call):
        mock_call.return_value = None
        configuration = {'TWILIO_ACCOUNT_SID': self.configure.account_sid,
                         'TWILIO_AUTH_TOKEN': self.configure.auth_token,
                         'TWILIO_APP_SID': self.configure.app_sid,
                         'TWILIO_CALLER_ID': self.configure.phone_number}

        self.configure.setHerokuEnvironmentVariables(**configuration)
        args, kwargs = mock_call.call_args
        self.assertTrue("heroku" in args[0],
                        "Heroku toolbelt not present in call: "
                        "{0}".format(args[0]))
        self.assertTrue("config:add" in args[0],
                        "Config:add not present in call: "
                        "{0}".format(args[0]))

        config = ["{0}={1}".format(k, v) for k, v in configuration.items()]
        for item in config:
            self.assertTrue(item in args[0],
                            "Missing config from call_args: {0} Instead got: "
                            "{0}".format(item, args[0]))


class MiscellaneousTest(unittest.TestCase):
    def test_configureWithoutAccountSid(self):
        test = configure.Configure(account_sid=None, auth_token=None,
                                   phone_number=None, app_sid=None)
        self.assertRaises(configure.ConfigurationError,
                          test.start)

    def test_configureWithoutAuthToken(self):
        test = configure.Configure(account_sid='ACxxxxxxx', auth_token=None,
                                   phone_number=None, app_sid=None)
        self.assertRaises(configure.ConfigurationError,
                          test.start)


class InputTest(ConfigureTest):
    @patch('twilio.rest.resources.Applications')
    @patch('twilio.rest.resources.Application')
    def test_createNewTwiMLAppWtfInput(self, MockApp, MockApps):
        # Mock the Applications resource and its create method.
        self.configure.client.applications = MockApps.return_value
        self.configure.client.applications.create.return_value = \
            MockApp.return_value

        # Mock our input
        configure.raw_input = Mock()
        configure.raw_input.return_value = 'wtf'

        # Test / Assert
        self.assertRaises(configure.ConfigurationError,
                          self.configure.createNewTwiMLApp,
                          self.configure.voice_url,
                          self.configure.sms_url)
        count = configure.raw_input.call_count
        self.assertTrue(configure.raw_input.call_count == 3, "Prompt did "
                        "not appear three times, instead: %i".format(count))
        self.assertFalse(self.configure.client.applications.create.called,
                         "Unexpected request to create AppSid made.")

    @patch('twilio.rest.resources.PhoneNumbers')
    @patch('twilio.rest.resources.PhoneNumber')
    def test_purchasePhoneNumberWtfInput(self, MockPhoneNumbers,
                                         MockPhoneNumber):
        # Mock the PhoneNumbers resource and its search and purchase methods
        mock_phone_number = MockPhoneNumber.return_value
        mock_phone_number.phone_number = self.configure.phone_number
        self.configure.client.phone_numbers = MockPhoneNumbers.return_value
        self.configure.client.phone_numbers.purchase = mock_phone_number

        # Mock our input.
        configure.raw_input = Mock()
        configure.raw_input.return_value = 'wtf'

        # Test / Assert
        self.assertRaises(configure.ConfigurationError,
                          self.configure.purchasePhoneNumber)
        self.assertTrue(configure.raw_input.call_count == 3, "Prompt did "
                        "not appear three times, instead: %i" %
                        configure.raw_input.call_count)
        self.assertFalse(self.configure.client.phone_numbers.purchase.called,
                         "Unexpected request to create AppSid made.")

    @patch('twilio.rest.resources.PhoneNumbers')
    @patch('twilio.rest.resources.PhoneNumber')
    def test_purchasePhoneNumberWtfInputConfirm(self,
                                                MockPhoneNumbers,
                                                MockPhoneNumber):
        # Mock the PhoneNumbers resource and its search and purchase methods
        mock_phone_number = MockPhoneNumber.return_value
        mock_phone_number.phone_number = self.configure.phone_number
        self.configure.client.phone_numbers = MockPhoneNumbers.return_value
        self.configure.client.phone_numbers.purchase = mock_phone_number

        # Mock our input.
        configure.raw_input = Mock()
        configure.raw_input.side_effect = ['y', 'wtf', 'wtf', 'wtf']

        # Test / Assert
        self.assertRaises(configure.ConfigurationError,
                          self.configure.purchasePhoneNumber)
        self.assertTrue(configure.raw_input.call_count == 4, "Prompt did "
                        "not appear three times, instead: %i" %
                        configure.raw_input.call_count)
        self.assertFalse(self.configure.client.phone_numbers.purchase.called,
                         "Unexpectedly requested phone number purchase.")


class CommandLineTest(unittest.TestCase):
    def test_account_sid(self):
        parser = configure.parse_args(['-SACxxx'])
        self.assertEquals(parser.account_sid, 'ACxxx')

    def test_new_phone_number(self):
        parser = configure.parse_args(['--new'])
        self.assertEquals(parser.phone_number, None)

    def test_custom_domain(self):
        parser = configure.parse_args(['-dtwilio.com'])
        self.assertEquals(parser.host, "twilio.com")

    def test_debug(self):
        parser = configure.parse_args(['-D'])
        self.assertTrue(parser.logger.level, logging.DEBUG)
