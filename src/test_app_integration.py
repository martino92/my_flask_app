#! /usr/bin/env python

import unittest
from app import app

class TestAppIntegration(unittest.TestCase):
    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    def test_form_submission(self):
        # Test the full form submission process
        # Step 1: Get the form
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<form action="/echo_user_input" method="POST">', response.data)

        # Step 2: Submit the form
        response = self.app.post('/echo_user_input', data=dict(user_input='Integration Test'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You entered Integration Test', response.data)

if __name__ == '__main__':
    unittest.main()
