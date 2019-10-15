import unittest
import data_import as datimp
from datetime import date


def create_test_csvs():
    with open('static_test.csv', 'w') as f:
        f.write('Id,time,value\n')
        for i in range(100):
            f.write(str(i)+','+str(date.today())+','+str(10)+'\n')
            
    with open('bad_date_test.csv', 'w') as f:
        f.write('Id,time,value\n')
        f.write(str(0)+','+str(1)+','+str(10)+'\n')

    with open('bad_value_test.csv', 'w') as f:
        f.write('Id,time,value\n')
        f.write(str(0)+','+str(date.today())+','+'blah'+'\n')
        
    with open('high_low_test.csv', 'w') as f:
        f.write('Id,time,value\n')
        f.write(str(0)+','+str(date.today())+','+'low'+'\n')
        f.write(str(1)+','+str(date.today())+','+'high'+'\n')
        
    with open('skip_empty_value_test.csv', 'w') as f:
        f.write('Id,time,value\n')
        f.write(str(0)+','+str(date.today())+','+''+'\n')  
        f.write(str(1)+','+str(date.today())+','+'10'+'\n')  

    
    
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
    '''
    def test_bad_values(self):
        self.assertRaises(ValueError,datimp.ImportData,'bad_value_test.csv')
        
    def test_bad_date(self):
        self.assertRaises(ValueError,datimp.ImportData,'bad_date_test.csv')
    '''    
    def test_high_low(self):
        data=datimp.ImportData('high_low_test.csv',replace_high_low=True)
        self.assertEqual(data._value[0],40)
        self.assertEqual(data._value[1],300)
        
    def test_skip_empty_value(self):
        data=datimp.ImportData('skip_empty_value_test.csv')
        self.assertEqual(data._value[0],10)