import unittest
import data_import as datimp
from datetime import date


def create_test_csvs():
    with open('static_test.csv', 'w') as f:
        f.write('Id,time,value\n')
        for i in range(100):
            f.write(str(i)+','+str(date.today())+','+str(10)+'\n')
    
create_test_csvs()

        


class TestImportData(unittest.TestCase):
    
    #File Input Tests
    
    def test_file_not_found(self):
        self.assertRaises(TypeError,datimp.ImportData,None)
    def test_bad_input_type(self):
        self.assertRaises(TypeError,datimp.ImportData,1)
        self.assertRaises(TypeError,datimp.ImportData,[1,12,3,4])
        self.assertRaises(TypeError,datimp.ImportData,1.0000)
    def test_file_doesnotexist(self):
        self.assertRaises(FileNotFoundError,datimp.ImportData,'no_file.csv')
    
    #File Value Tests
    
    def test_file_values(self):
        data=datimp.ImportData('static_test.csv')
        self.assertEqual(sum(data._value),1000)