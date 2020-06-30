import unittest

from vse.core.task import VSETaskSchema, VSETask, ValidationError


class VSETaskTestCase(unittest.TestCase):
    def test_schema_load(self):
        task = VSETaskSchema().load(
            {
                "action": "test_handler",
                "description": "Test Handler for APP",
                "expectation": True,
                "params": {
                    "poke": True
                }
            }
        )
        self.assertIsInstance(task, VSETask)
        self.assertIsInstance(task.to_dict(), dict)

        # Demonstrates the minimum needed to create a task.
        task = VSETaskSchema().load(
            {
                "action": "test_handler",
                "params": {
                    "poke": True
                }
            }
        )
        self.assertIsInstance(task, VSETask)
        self.assertIsInstance(task.to_dict(), dict)

    def test_schema_invalid_action(self):
        with self.assertRaises(ValidationError):
            VSETaskSchema().load(
                {
                    "action": "bad_handler",
                    "description": "Test Handler for APP",
                    "expectation": True,
                    "params": {
                        "poke": True
                    }
                }
            )

    def test_required_fields(self):
        with self.assertRaises(ValidationError):
            VSETaskSchema().load(
                {
                    # "action": "bad_handler", Missing Required Key
                    "description": "Test Handler for APP",
                    "expectation": True,
                    "params": {
                        "poke": True
                    }
                }
            )

    def test_default_fields(self):
        # Tests default expectation value
        task = VSETaskSchema().load(
            {
                "action": "test_handler",
                "description": "test description",
                "params": {
                    "poke": True
                }
            }
        )
        self.assertTrue(task.expectation)
        self.assertEqual(task.description, "test description")


if __name__ == '__main__':
    unittest.main()
