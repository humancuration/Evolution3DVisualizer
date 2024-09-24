# test_data_loader.py

import unittest
from mod_data_loader import load_data

class TestDataLoader(unittest.TestCase):
    def test_load_csv(self):
        data = load_data('data_sample_dataset.csv')
        self.assertIsInstance(data, list)
        if data:
            self.assertIsInstance(data[0], dict)
    
    def test_load_nonexistent_file(self):
        data = load_data('nonexistent_file.csv')
        self.assertEqual(data, [])
    
    def test_load_invalid_format(self):
        data = load_data('data_sample_dataset.invalid')
        self.assertEqual(data, [])

if __name__ == '__main__':
    unittest.main()
