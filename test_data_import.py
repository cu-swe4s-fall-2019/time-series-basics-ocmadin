import unittest
import data_import as datimp
from datetime import datetime
import os

def create_test_csvs():
    with open('static_test.csv', 'w') as f:
        f.write('Id,time,value\n')
        for i in range(100):
            f.write(str(i)+','+str(datetime.now())+','+str(10)+'\n')
            
    with open('bad_date_test.csv', 'w') as f:
        f.write('Id,time,value\n')
        f.write(str(0)+','+str(1)+','+str(10)+'\n')

    with open('bad_value_test.csv', 'w') as f:
        f.write('Id,time,value\n')
        f.write(str(0)+','+str(datetime.now())+','+'blah'+'\n')
        
    with open('high_low_test.csv', 'w') as f:
        f.write('Id,time,value\n')
        f.write(str(0)+','+str(datetime.now())+','+'low'+'\n')
        f.write(str(1)+','+str(datetime.now())+','+'high'+'\n')
        
    with open('skip_empty_value_test.csv', 'w') as f:
        f.write('Id,time,value\n')
        f.write(str(0)+','+str(datetime.now())+','+''+'\n')  
        f.write(str(1)+','+str(datetime.now())+','+'10'+'\n')  

    
    






class TestImportData(unittest.TestCase):
    create_test_csvs()
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

        
    def test_no_key(self):
        data=datimp.ImportData('high_low_test.csv',replace_high_low=True)
        self.assertRaises(TypeError,data.linear_search_value,None)
    
    def test_bad_key_type(self):
        data=datimp.ImportData('high_low_test.csv',replace_high_low=True)
        self.assertRaises(TypeError,data.linear_search_value,[1,1,1])
        self.assertRaises(TypeError,data.linear_search_value,1)
        self.assertRaises(TypeError,data.linear_search_value,'text')
        
    def test_search_miss(self):
        data=datimp.ImportData('smallData/cgm_small.csv')
        self.assertEqual(data.linear_search_value(datetime.now()),-1)
        
    def test_search_hit(self):
        data=datimp.ImportData('smallData/cgm_small.csv')
        self.assertEqual(data.linear_search_value(data._time[0]),data._value[0])

    
    def test_skip_empty_value(self):
        data=datimp.ImportData('skip_empty_value_test.csv')
        self.assertEqual(data._value[0],10)
        self.remove_test_csvs()
        
    
        
    def remove_test_csvs(self):
        os.remove('skip_empty_value_test.csv')
        os.remove('high_low_test.csv')
        os.remove('bad_value_test.csv')
        os.remove('bad_date_test.csv')
        os.remove('static_test.csv')
