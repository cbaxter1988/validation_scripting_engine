import unittest
from pprint import pprint

from vse.core import VSE, VSEActionMapper, VSESchema, Handler, VSEAudit, VSEResult
from vse.core.task import VSETask, VSETaskSchema
from vse.handlers.base import IHandler
from vse.handlers.base import HandlerResult


class VSETestCase(unittest.TestCase):

    def test_run(self):
        vse = VSE()

        audit1 = VSEAudit(
            target="192.168.1.5",
            name="My Core Switch Audit",
            fail_limit=2
        )
        audit2 = VSEAudit(
            target="192.168.1.10",
            name="My Core Router Audit",
            fail_limit=0
        )

        task1 = VSETask(**
                        {
                            "action": "test_handler",
                            "description": "Test My API",
                            "params": {
                                "poked": False
                            },
                            "expectation": True
                        }
                        )

        task2 = VSETask(**
                        {
                            "action": "test_handler",
                            "description": "Test My API",
                            "params": {
                                "poked": True
                            },
                            "expectation": False
                        }
                        )

        audit1.add_task(task1)
        audit1.add_task(task2)

        audit2.add_task(task1)
        audit2.add_task(task2)

        vse.add_audit(audit1)
        vse.add_audit(audit2)
        results = vse.run()

        self.assertEqual(len(vse.results), 2)

        for res in results:
            self.assertIsInstance(res, VSEResult)

    def test_add_audit(self):
        vse = VSE()

        audit1 = VSEAudit(
            target="192.168.1.1",
            name="My Core Audit",
            fail_limit=2
        )

        self.assertTrue(vse.add_audit(audit1))

        # Edge Case, test for bad data type for audit data.
        self.assertFalse(vse.add_audit("BAD_DATA"))

    def test_remove_audit(self):
        vse = VSE()

        audit1 = VSEAudit(
            target="192.168.1.1",
            name="My Core Audit",
            fail_limit=2
        )

        self.assertFalse(vse.remove_audit(audit1))

        vse.add_audit(audit1)

        self.assertTrue(vse.add_audit(audit1))

    def test_get_task_handler(self):
        vse = VSE()

        task1 = VSETask(**
                        {
                            "action": "test_handler",
                            "params": {
                                "poked": False
                            },
                            "expectation": True
                        }
                        )

        h = vse.get_task_handler(task1)
        self.assertIsInstance(h, Handler)
        self.assertIsInstance(h, IHandler)

        # help(vse)


if __name__ == '__main__':
    unittest.main(verbosity=2)
