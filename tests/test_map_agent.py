import unittest
from vse.core.mapping_agent import VSEMapAgent, MappingAgentError
from vse.core.task import make_vse_task
from vse.handlers import TestHandlerParams, TestHandler, Handler


class BadClass:
    pass


class MapAgentTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.task = make_vse_task(
            {
                "action": "test_handler",
                "description": "Test Handler for APP",
                "expectation": True,
                "params": {
                    "poke": True
                }
            }
        )

    def test_register_handler(self):
        ma = VSEMapAgent()

        with self.assertRaises(MappingAgentError):
            ma.register_handler("test_handler", "BadType", "BadType")

        with self.assertRaises(MappingAgentError):
            ma.register_handler("test_handler", BadClass(), BadClass())

        with self.assertRaises(MappingAgentError):
            ma.register_handler("test_handler", TestHandler, TestHandlerParams())

        with self.assertRaises(MappingAgentError):
            ma.register_handler("test_handler", TestHandler(), TestHandlerParams)

        self.assertTrue(ma.register_handler("test_handler", TestHandler, TestHandlerParams))

        self.assertEqual(1, ma.get_handler_count())

    def test_get_handler(self):
        ma = VSEMapAgent()

        ma.register_handler("test_handler", TestHandler, TestHandlerParams)

        resp = ma.get_handler(self.task.action, self.task)
        self.assertIsInstance(resp, Handler)

        with self.assertRaises(MappingAgentError):
            ma.get_handler("bad_request", self.task)

    def test_update(self):
        class UpdateTestHandler(TestHandler):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

        class UpdateHandlerParams(TestHandlerParams):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

        ma = VSEMapAgent()
        ma.register_handler("test_handler", TestHandler, TestHandlerParams)

        result = ma.update("test_handler", UpdateTestHandler, UpdateHandlerParams)
        self.assertTrue(result)
        #
        handler = ma.get_handler("test_handler", self.task)
        self.assertTrue(handler.__class__ == UpdateTestHandler)
        #
        result = ma.update("bad_handler", UpdateTestHandler, UpdateHandlerParams)
        self.assertFalse(result)

        with self.assertRaises(MappingAgentError):
            ma.update("test_handler", UpdateTestHandler(), UpdateHandlerParams)
            ma.update("test_handler", UpdateTestHandler, UpdateHandlerParams())

    def test_delete_handler(self):
        ma = VSEMapAgent()

        ma.register_handler("test_handler", TestHandler, TestHandlerParams)

        resp = ma.delete_handler("test_handler")
        self.assertTrue(resp)

        resp = ma.delete_handler("bad_handler")
        self.assertFalse(resp)


if __name__ == '__main__':
    unittest.main()
