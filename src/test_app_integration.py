#! /usr/bin/env python

import unittest
from app import app, init_db

class TestAppIntegration(unittest.TestCase):
    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True
        init_db()  # Initialize the database before each test

    def test_workflow(self):
        # Step 1: Check the main page
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Post Statistics</h1>', response.data)

        # Step 2: Fetch posts
        response = self.app.post('/fetch_posts')
        self.assertIn(response.status_code, [200, 202])
        data = response.get_json()
        self.assertIn('message', data)
        self.assertIn('Posts', data['message'])

        # Step 3: Check statistics
        response = self.app.get('/api/stats')
        self.assertEqual(response.status_code, 200)
        stats = response.get_json()
        self.assertIn('total_posts', stats)
        self.assertIn('avg_title_length', stats)
        self.assertIn('avg_body_length', stats)

if __name__ == '__main__':
    unittest.main()
