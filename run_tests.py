import unittest

from tests import (
    test_vse,
    test_mapping_agent,
    test_vse_audit,
    test_vse_audit_task,
    test_wrapper_ssh_cmd,
    test_ssh_config
)

# Creates loader and empty test suite.
loader = unittest.TestLoader()
suite = unittest.TestSuite()


def load_tests():
    suite.addTests(loader.loadTestsFromModule(test_vse))
    suite.addTests(loader.loadTestsFromModule(test_mapping_agent))
    suite.addTests(loader.loadTestsFromModule(test_vse_audit))
    suite.addTests(loader.loadTestsFromModule(test_vse_audit_task))
    suite.addTests(loader.loadTestsFromModule(test_wrapper_ssh_cmd))
    suite.addTests(loader.loadTestsFromModule(test_ssh_config))


def run_tests():
    runner = unittest.TextTestRunner(verbosity=1)
    runner.run(suite)


if __name__ == "__main__":
    load_tests()
    run_tests()
