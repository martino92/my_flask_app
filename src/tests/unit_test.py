#! /usr/bin/env python

import unittest

from data_process import DataProcess

class TestFilterAndProcessing(unittest.TestCase):
    '''
    setUp method is used to instantiate the object we are testing
    '''
    def setUp(self):
        self.data = [
            {'id': 1, 'name': 'Alice', 'age': 16},
            {'id': 2, 'name': 'Bob', 'age': 18},
            {'id': 3, 'name': 'Charlie', 'age': 20},
        ]
        self.dp = DataProcess(self.data)

    def test_filter_and_processing(self):
        # define a processing function
        def process_func(data):
            data['age_category'] = 'Adult' if data['age'] >= 18 else 'Minor'
            return data
        
        expected_result = [
            {'id': 1, 'name': 'Alice', 'age': 16, 'age_category': 'Minor'},
            {'id': 2, 'name': 'Bob', 'age': 18, 'age_category': 'Adult'},
            {'id': 3, 'name': 'Charlie', 'age': 20, 'age_category': 'Adult'},
        ]

        result = self.dp.filter_and_process(filter_key='age', filter_value=3, process_function=process_func)

        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()