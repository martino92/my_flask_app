#！/usr/bin/env python

import unittest
from database import Database
from data_process import DataProcess

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.data = {}
        self.dp = DataProcess(self.data)
    
    def test_add_and_retrieve(self):
        key, value = 'test_key', 'test_value'
        self.dp.add_to_database(key, value)
        result = self.dp.db.retrieve(key)
        self.assertEqual(result, value)

if __name__ == '__main__':
    unittest.main()


