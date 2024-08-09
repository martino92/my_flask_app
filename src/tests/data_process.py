#! /usr/bin/env python

from database import Database

class DataProcess:
    def __init__(self, data):
        self.data = data
        self.db = Database()
    
    # for illustrating unit test
    def filter_and_process(self, filter_key, filter_value, process_function):
        filtered_data = [data for data in self.data if data.get(filter_key) >= filter_value]

        processed_data = [process_function(data) for data in filtered_data]

        return processed_data
    
    # for illustrating integration test
    def add_to_database(self, key, value):
        self.db.insert(key, value)

        return self.db.retrieve(key)


