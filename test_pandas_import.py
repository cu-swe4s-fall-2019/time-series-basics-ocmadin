import unittest
import pandas_import

class TestImportData(unittest.TestCase):
    def test_file_import(self):
        self.assertRaises(TypeError, pandas_import.import_data,None)
        self.assertRaises(ImportError, pandas_import.import_data,'data.txt')
        self.assertRaises(FileNotFoundError, pandas_import.import_data,'fake_data.csv')