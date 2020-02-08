""" tests script """

import unittest
import subprocess
import http.client
import random


class WebTestCase(unittest.TestCase):
    """tests for the WSGI Calculator"""

    def setUp(self):
        self.server_process = subprocess.Popen(
            [
                "python",
                "calculator.py"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def tearDown(self):
        self.server_process.kill()
        self.server_process.communicate()

    def get_response(self, url):
        """
        Helper function to get a response from a given url, using http.client
        """
        try:
            conn = http.client.HTTPConnection('localhost:8080')
            # conn = http.client.HTTPConnection('localhost:9999')
            conn.request('GET', url)

            response = conn.getresponse()
            self.assertEqual(200, response.getcode())

            conn.close()

            return response

        except ConnectionRefusedError as err:
            return print("script re-runs to establish connection: ", err)

    def test_add(self):
        """
        A call to /add/a/b yields a + b
        """

        a = random.randint(100, 10000)
        b = random.randint(100, 10000)

        path = "/add/{}/{}".format(a, b)

        response = self.get_response(path)
        self.assertEqual(200, response.getcode())

        self.assertIn(str(a + b).encode(), response.read())

    def test_multiply(self):
        """
        A call to /multiply/a/b yields a*b
        """

        a = random.randint(100, 10000)
        b = random.randint(100, 10000)

        path = "/multiply/{}/{}".format(a, b)

        response = self.get_response(path)
        self.assertEqual(200, response.getcode())

        self.assertIn(str(a*b).encode(), response.read())

    def test_subtract_positive_result(self):
        """
        A call to /subtract/a/b yields a - b, for a > b
        """

        a = random.randint(10000, 100000)
        b = random.randint(100, 1000)

        path = "/subtract/{}/{}".format(a, b)

        response = self.get_response(path)
        self.assertEqual(200, response.getcode())

        self.assertIn(str(a - b).encode(), response.read())

    def test_subtract_negative_result(self):
        """
        A call to /subtract/a/b yields a - b, for a < b
        """

        a = random.randint(100, 1000)
        b = random.randint(10000, 100000)

        path = "/subtract/{}/{}".format(a, b)

        response = self.get_response(path)
        self.assertEqual(200, response.getcode())

        self.assertIn(str(a - b).encode(), response.read())

    def test_divide(self):
        """
        A call to /divide/a/b yields a/b, for a % b = 0
        """

        result = random.randint(2, 10)

        b = random.randint(100, 1000)
        a = result * b

        path = "/divide/{}/{}".format(a, b)

        response = self.get_response(path)
        self.assertEqual(200, response.getcode())

        self.assertIn(str(result).encode(), response.read())

    def test_index_instructions(self):
        """
        The index page at the root of the server shall include instructions
        on how to use the page.
        """

        response = self.get_response('/')
        self.assertEqual(200, response.getcode())

        # We're just testing if the word "add" is present in the index
        self.assertIn("add".encode(), response.read())

    # ----------------------------------------
    def test_division_by_zero(self):
        """
        Tests the case when the denominator of fraction is zero
        """
        conn = http.client.HTTPConnection('localhost:8080')

        a = random.uniform(100, 1000)
        b = 0
        path = "/divide/{}/{}".format(a, b)

        conn.request('GET', path)
        response = conn.getresponse()
        conn.close()

        self.assertEqual(400, response.getcode())

    def test_name_error(self):
        """
        Tests the case when the path contains letters rather than numbers
        for addition operation
        """
        conn = http.client.HTTPConnection('localhost:8080')

        a = random.uniform(100, 1000)
        b = 'a'
        path = "/add/{}/{}".format(a, b)

        conn.request('GET', path)
        response = conn.getresponse()
        self.assertEqual(500, response.getcode())

        conn.close()

    def test_missing_input(self):
        """
        Tests the case when the path is missing a number
        for addition operation
        """
        conn = http.client.HTTPConnection('localhost:8080')

        a = random.uniform(100, 1000)
        b = ''
        path = "/add/{}/{}".format(a, b)

        conn.request('GET', path)
        response = conn.getresponse()
        self.assertEqual(200, response.getcode())

        conn.close()
    # ----------------------------------------


if __name__ == '__main__':
    unittest.main()

# =============================================
# ====== Sample run ===========================
# (base) C:\Users\Florentin\Desktop\UW3\L4\wsgi-calculator>python -m unittest -vv tests.py
# test_add (tests.WebTestCase) ... ok
# test_divide (tests.WebTestCase) ... ok
# test_division_by_zero (tests.WebTestCase) ... ok
# test_index_instructions (tests.WebTestCase) ... ok
# test_missing_input (tests.WebTestCase) ... ok
# test_multiply (tests.WebTestCase) ... ok
# test_name_error (tests.WebTestCase) ... ok
# test_subtract_negative_result (tests.WebTestCase) ... ok
# test_subtract_positive_result (tests.WebTestCase) ... ok

# ----------------------------------------------------------------------
# Ran 9 tests in 9.386s

# OK
