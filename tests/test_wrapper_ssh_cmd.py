import unittest
from unittest.mock import patch

import requests

from vse.wrappers.ssh_cmd import SSHCMDWrapper, WrapperResult, SSHCMDWrapperSchema, ipaddress, \
    ValidationError


class WrapperCase(unittest.TestCase):

    def setUp(self):
        self.schema = SSHCMDWrapperSchema()

    @patch("requests.post")
    def test_wrapper_ssh_cmd_send_case1(self, mocked_post):
        '''
        Mocks as if status_code == 200 is received from server.

        :return:
        '''

        class MockedPostRequest(object):
            status_code = 200

            def json(self):
                return {
                    "data": ""
                }

        mocked_post.return_value = MockedPostRequest()

        # print(mocked_post)
        wrapper = self.schema.load(
            {
                "target": "192.168.1.2",
                "nodeType": "cisco_ios",
                "username": "cisco",
                "password": "cisco",
                "cmd": "show run",
            }
        )

        result = wrapper.send()

        self.assertEqual(mocked_post.called, True)
        self.assertIsInstance(result, WrapperResult)
        self.assertTrue(result.status)

    @patch("requests.post")
    def test_wrapper_ssh_cmd_send_case2(self, mocked_post):
        '''
        Mocks as if status_code == 400 is received from server.
        :return:
        '''

        class MockedPostRequest(object):
            status_code = 400

            def json(self):
                return {
                    "data": ""
                }

        mocked_post.return_value = MockedPostRequest()

        wrapper = self.schema.load(
            {
                "target": "192.168.1.2",
                "nodeType": "cisco_ios",
                "username": "cisco",
                "password": "cisco",
                "cmd": "show run",
            }
        )

        result = wrapper.send()

        self.assertEqual(mocked_post.called, True)
        self.assertIsInstance(result, WrapperResult)
        self.assertFalse(result.status)

    @patch("requests.post")
    def test_wrapper_ssh_cmd_send_case4(self, mocked_post):
        '''
        Mocks as if Timeout is received from Server, Expected response
        :return:
        '''

        mocked_post.side_effect = requests.Timeout

        wrapper: SSHCMDWrapper = self.schema.load(
            {
                "target": "192.168.1.2",
                "nodeType": "cisco_ios",
                "username": "cisco",
                "password": "cisco",
                "cmd": "show run",
            }
        )

        result = wrapper.send()

        self.assertEqual(mocked_post.called, True)
        self.assertIsInstance(result, WrapperResult)
        self.assertFalse(result.status)

    @patch("requests.post")
    def test_wrapper_ssh_cmd_send_case5(self, mocked_post):
        '''
        Mocks as if no status code is received from Server
        :return:
        '''

        class MockedPostRequest(object):
            status_code = None

            def json(self):
                return {
                    "data": ""
                }

        mocked_post.return_value = MockedPostRequest()

        wrapper = self.schema.load(
            {
                "target": "192.168.1.2",
                "nodeType": "cisco_ios",
                "username": "cisco",
                "password": "cisco",
                "cmd": "show run",
            }
        )

        result = wrapper.send()

        self.assertEqual(mocked_post.called, True)
        self.assertIsInstance(result, WrapperResult)
        self.assertFalse(result.status)

    def test_wrapper_ssh_cmd_send_case3(self):
        '''
        Test for Invalid IP address and nodeType

        :return:
        '''

        with self.assertRaises(ipaddress.AddressValueError):
            self.schema.load(
                {
                    "target": "192.168.1.2555",
                    "nodeType": "cisco_ios",
                    "username": "cisco",
                    "password": "cisco",
                    "cmd": "show run",
                }
            )

        with self.assertRaises(ValidationError):
            self.schema.load(
                {
                    "target": "192.168.1.255",
                    "nodeType": "BAD_NODE_TYPE",
                    "username": "cisco",
                    "password": "cisco",
                    "cmd": "show run",
                }
            )

    def test_wrapper_ssh_cmd_send_case6(self):
        """
        Test Required Data feilds for the schema

        :return:
        """

        with self.assertRaises(ValidationError):
            self.schema.load(
                {
                    "MISSING": "REQUIRED_FIELDS",

                }
            )


if __name__ == '__main__':
    unittest.main()
