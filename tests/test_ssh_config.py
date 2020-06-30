import ipaddress
import unittest
from unittest.mock import patch

from marshmallow import ValidationError

from vse.wrappers.ssh_config import SSHConfigWrapper, WrapperResult, SSHConfigWrapperSchema


class SSHConfigWrapperTestCase(unittest.TestCase):

    def setUp(self):
        self.schema = SSHConfigWrapperSchema()

    @patch("requests.post")
    def test_wrapper_ssh_config_case1(self, mocked_post):
        '''
        Mocks as if the server return status_code == 200

        :return:
        '''

        class MockedPostRequest(object):
            status_code = 200

            def json(self):
                return {
                    "data": ""
                }

        mocked_post.return_value = MockedPostRequest()

        wrapper: SSHConfigWrapper = self.schema.load(
            {
                "target": "1.1.1.1",
                "nodeType": "cisco_ios",
                "username": "cisco",
                "password": "cisco",
            }
        )

        result = wrapper.send()

        self.assertIsInstance(wrapper.send(), WrapperResult)
        self.assertEqual(mocked_post.called, True)
        self.assertTrue(result.status)

    def test_wrapper_ssh_config_case2(self):
        """
        Tests required fields for Schema.
        """

        with self.assertRaises(ValidationError):
            self.schema.load(
                {
                    "BAD": "DATA"
                }
            )

    def test_wrapper_ssh_config_case3(self):
        """
        Tests IP Address validation.

        """

        with self.assertRaises(ipaddress.AddressValueError):
            self.schema.load(
                {
                    "target": "1.1.1.1555",
                    "nodeType": "cisco_ios",
                    "username": "cisco",
                    "password": "cisco",
                }
            )

    def test_wrapper_ssh_config_case4(self):
        """
        Tests Device Type validation.

        """
        with self.assertRaises(ValidationError):
            self.schema.load(
                {
                    "target": "1.1.1.1",
                    "nodeType": "cisco_iosss",
                    "username": "cisco",
                    "password": "cisco",
                }
            )

    def test_wrapper_ssh_config_case5(self):
        """
        Mocks if the self._send() returns a bad type,

        """

        controller = self.schema.load(
            {
                "target": "1.1.1.1",
                "nodeType": "cisco_ios",
                "username": "cisco",
                "password": "cisco",
            }
        )

        with patch('vse.wrappers.ssh_config.SSHConfigWrapper._send') as mocked_send:
            mocked_send.return_value = "BAD_DATA"
            result = controller.send()

            self.assertTrue(mocked_send.called)
            self.assertEqual(result.msg, "Invalid Return Type Received from self._send().")
            self.assertIsInstance(result, WrapperResult)
            self.assertFalse(result.status)


if __name__ == '__main__':
    unittest.main()
