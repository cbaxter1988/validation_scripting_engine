import unittest

from vse.core.mapping_agent import VSEActionMapper, Handler, HandlerResult, DefaultHandler
from vse.core.task import VSETask
from vse.core.exceptions import InvalidHandlerErr


class VSEActionMapperTestCase(unittest.TestCase):
    def test_get_handler(self):
        """
        Basic test of the VSEActionMapper.get_handler(VSEtask)
        """
        mapper = VSEActionMapper()

        task1 = VSETask(**
                        {
                            "action": "test_handler",
                            "params": {
                                "poked": False
                            },
                            "expectation": True
                        }
                        )

        h = mapper.get_handler(task1)
        self.assertIsInstance(h, Handler)

        res = h.execute()
        self.assertIsInstance(res, HandlerResult)

    def test_get_handler_1(self):
        """
        Test if bad_action is provided, InvalidHandler Exception is raised.
        """
        mapper = VSEActionMapper()

        task1 = VSETask(**
                        {
                            "action": "bad_handler",
                            "params": {},
                            "expectation": True
                        }
                        )

        with self.assertRaises(InvalidHandlerErr):
            mapper.get_handler(task1)

        with self.assertRaises(InvalidHandlerErr):
            mapper.get_handler("BAD_REQ_TYPE")


if __name__ == '__main__':
    unittest.main()
