#! /usr/bin/env python

import unittest
from app import app, init_db

class TestAppUnit(unittest.TestCase):
    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True
        init_db()

    def test_main_route(self):
        # Test the main route
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Post Statistics</h1>', response.data)
        self.assertIn(b'<button onclick="fetchPosts()">Fetch Posts</button>', response.data)

    def test_fetch_posts_route(self):
        # Test the fetch_posts route
        response = self.app.post('/fetch_posts')
        self.assertIn(response.status_code, [200, 202])
        data = response.get_json()
        self.assertIn('message', data)
        self.assertIn('Posts', data['message'])

    def test_api_stats_route(self):
        # Test the api_stats route
        response = self.app.get('/api/stats')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('total_posts', data)
        self.assertIn('avg_title_length', data)
        self.assertIn('avg_body_length', data)

if __name__ == '__main__':
    unittest.main()
