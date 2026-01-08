from unittest import TestSuite, TestLoader, TextTestRunner

from tests import test1, test_util, test_visual

MODULES = test1, test_util, test_visual


def get_suite() -> TestSuite:
    suite = TestSuite()
    for m in MODULES:
        suite.addTests(
            TestLoader().loadTestsFromModule(m),
        )
    return suite


if __name__ == '__main__':
    test_suite = get_suite()
    runner = TextTestRunner(verbosity=2)
    runner.run(test_suite)
