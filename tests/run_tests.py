from unittest import TestLoader, TextTestRunner
from api_test import APITestCase

if __name__ == "__main__":
    testRunner = TextTestRunner()
    api_tests = APITestCase()
    test_results = testRunner.run(api_tests)

    if test_results.wasSuccessful():
        exit(0)
    else:
        exit(1)
