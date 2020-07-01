import unittest
from vse.core.mapping_agent import VSEMapAgent, MappingAgentError
from vse.handlers import TestHandlerParams, TestHandler


class BadClass:
    pass


class MapAgentTestCase(unittest.TestCase):
    def test_add_handler(self):
        ma = VSEMapAgent()

        with self.assertRaises(MappingAgentError):
            ma.add_handler("test_handler", BadClass, BadClass)

        with self.assertRaises(MappingAgentError):
            ma.add_handler("test_handler", "BadType", "BadType")

        with self.assertRaises(MappingAgentError):
            ma.add_handler("test_handler", BadClass(), BadClass())

        self.assertTrue(ma.add_handler("test_handler", TestHandler, TestHandlerParams()))

        self.assertEqual(1, ma.get_handler_count())

    def test_get_handler(self):
        ma = VSEMapAgent()

        ma.add_handler("test_handler", TestHandler, TestHandlerParams())

        resp = ma.get_handler("test_handler")
        self.assertIsInstance(resp, dict)

        resp = ma.get_handler("bad_request")
        self.assertEqual(resp, None)

    def test_update(self):
        class UpdateTestHandler(TestHandler):
            pass

        class UpdateHandlerParams(TestHandlerParams):
            pass

        ma = VSEMapAgent()
        ma.add_handler("test_handler", TestHandler, TestHandlerParams())

        self.assertTrue(ma.update("test_handler", UpdateTestHandler, UpdateHandlerParams()))

        handler = ma.get_handler("test_handler")
        self.assertTrue(handler['handler'] == UpdateTestHandler)
        self.assertIsInstance(handler['params_schema'], UpdateHandlerParams)

        self.assertFalse(ma.update("bad_handler", UpdateTestHandler, UpdateHandlerParams()))

    def test_delete_handler(self):
        ma = VSEMapAgent()

        ma.add_handler("test_handler", TestHandler, TestHandlerParams())

        resp = ma.delete_handler("test_handler")
        self.assertTrue(resp)

        resp = ma.delete_handler("bad_handler")
        self.assertFalse(resp)


if __name__ == '__main__':
    unittest.main()
