import unittest
from marshmallow.exceptions import ValidationError
from vse.core.audit import VSEAudit, VSETask, VSEAuditSchema, new_audit


class VSEAuditTestCase(unittest.TestCase):
    def test_add_task(self):
        task1 = VSETask(**
                        {
                            "action": "test_handler",
                            "params": {
                                "poked": False
                            },
                            "expectation": True
                        }
                        )

        audit = VSEAudit(
            **{
                "target": "192.168.1.1",
                "fail_limit": 0
            }
        )

        self.assertTrue(audit.add_task(task1))

        # Edged Case to check if adding duplicate task fails
        self.assertFalse(audit.add_task(task1))

    def test_del_task(self):
        audit = VSEAudit(
            **{
                "target": "192.168.1.1",
                "fail_limit": 0
            }
        )

        task1 = VSETask(**
                        {
                            "action": "test_handler",
                            "params": {
                                "poked": False
                            },
                            "expectation": True
                        }
                        )

        audit.add_task(task1)

        self.assertTrue(audit.del_task(task1))

    def test_has_task(self):
        audit = VSEAudit(
            **{
                "target": "192.168.1.1",
                "fail_limit": 0
            }
        )

        task1 = VSETask(**
                        {
                            "action": "test_handler",
                            "params": {
                                "poked": False
                            },
                            "expectation": True
                        }
                        )

        self.assertFalse(audit.has_task())

        audit.add_task(task1)

        self.assertTrue(audit.has_task())

    def test_to_dict(self):
        audit = VSEAudit(
            **{
                "target": "192.168.1.1",
                "description": "My Custom Audit",
                "fail_limit": 0
            }
        )

        audit.add_task(
            VSETask(**
                    {
                        "action": "test_handler",
                        "params": {
                            "poked": False
                        },
                        "expectation": True
                    }
                    )
        )

        self.assertIsInstance(audit.to_dict(), dict)

    def test_clear_task(self):
        audit = VSEAudit(
            **{
                "target": "192.168.1.1",
                "fail_limit": 0
            }
        )

        task1 = VSETask(**
                        {
                            "action": "test_handler",
                            "params": {
                                "poked": False
                            },
                            "expectation": True
                        }
                        )

        self.assertFalse(audit.clear_task())  # Checks if returns false if there are no Task to clear.

        self.assertEqual(len(audit.tasks), 0)

        audit.add_task(task1)
        self.assertEqual(len(audit.tasks), 1)

        audit.clear_task()
        self.assertEqual(len(audit.tasks), 0)

    def test_new_audit(self):
        audit_data = {
            "target": "192.168.1.1",
            "fail_limit": 0,
            "tasks": [
                {
                    "action": "test_handler",
                    "params": {
                        "poked": False
                    },
                    "expectation": True
                }
            ]
        }

        audit = new_audit(audit_data)

        self.assertIsInstance(audit, VSEAudit)
        self.assertEqual(len(audit.tasks), 1)

        with self.assertRaises(ValidationError):
            # Test ValidationError Raises when providing incomplete data model.
            del audit_data['target']
            # Checks for Invalid Audit Data
            new_audit(audit_data)


if __name__ == '__main__':
    unittest.main(verbosity=2)
