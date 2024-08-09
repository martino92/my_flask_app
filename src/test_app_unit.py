#! /usr/bin/env python

import unittest
from app import app

class TestAppUnit(unittest.TestCase):
    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    def test_main_route(self):
        # Test the main route
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<form action="/echo_user_input" method="POST">', response.data)

    def test_echo_input_route(self):
        # Test the echo_input route with a sample input
        response = self.app.post('/echo_user_input', data=dict(user_input='Hello, World!'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You entered Hello, World!', response.data)

if __name__ == '__main__':
    unittest.main()
