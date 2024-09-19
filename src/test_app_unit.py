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
        self.assertIn(b'<h1>Post Statistics</h1>', response.data)
        self.assertIn(b'<button onclick="fetchPosts()">Fetch Posts</button>', response.data)

    def test_fetch_posts_route(self):
        # Test the fetch_posts route
        response = self.app.post('/fetch_posts')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Posts are being fetched', response.data)

    def test_api_stats_route(self):
        # Test the api_stats route
        response = self.app.get('/api/stats')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'total_posts', response.data)
        self.assertIn(b'avg_title_length', response.data)
        self.assertIn(b'avg_body_length', response.data)

if __name__ == '__main__':
    unittest.main()
