import csv
import dateutil.parser
from os import listdir
from os.path import isfile, join
import argparse
import datetime
import numpy as np


class ImportData:
    def __init__(self, data_csv,replace_high_low=False):
        
        if data_csv is None:
            raise TypeError("ImportData: No input filepath provided")
            
        if not isinstance(data_csv,str):
            raise TypeError('ImportData: Filename must be string')
        
        self._time = []
        self._value = []

        with open(data_csv, "r") as fhandle:
            try:
                reader = csv.DictReader(fhandle)
            except FileNotFoundError:
                print('ImportData: File does not exist')
            for row in reader:
                try:
                    if row['time'] == '':
                        print('ImportData: Removing blank time value')
                        continue
                    self._time.append(dateutil.parser.parse(row['time']))
                except ValueError:
                    raise ValueError('ImportData: Bad time value')
                if replace_high_low is True:
                    if row['value'] == '':
                        print('ImportData: Removing blank value')
                        continue
                    if row['value'] == 'low':
                        self._value.append(int(40))
                        print('ImportData: Replacing "low" value with 40')
                    elif row['value'] == 'high':
                        self._value.append(int(300))
                        print('ImportData: Replacing "high" value with 300')
                    else:    
                        self._value.append(int(row['value']))
                else:
                    if row['value'] == '':
                        print('ImportData: Removing blank value')
                        continue
                    self._value.append(int(row['value']))
            fhandle.close()

        # open file, create a reader from csv.DictReader, and read input times and values

    def linear_search_value(self, key_time):
        if key_time is None:
            raise TypeError('ImportData.linear_search_value: No key value supplied')
            
        if not isinstance(key_time,datetime.datetime):
            raise TypeError('ImportData.linear_search_value: Key must be datetime.datetime data type')
            
        for i in range(len(self._time)):
            curr =  self._time[i]
            if key_time == curr:
                return self._value[i]
        print('invalid time')
        return -1
            
        # return list of value(s) associated with key_time
        # if none, return -1 and error message
        pass

    def binary_search_value(self,key_time):
        # optional extra credit
        # return list of value(s) associated with key_time
        # if none, return -1 and error message
        pass

def roundTimeArray(obj, res, repeat_operation='average'):
    
    if obj is None:
        raise TypeError('roundTimeArray: requires an ImportData object')
    if res is None:
        raise TypeError('roundTimeArray: requires a rounding resolution')
    if not isinstance(obj,ImportData):
        raise TypeError('roundTimeArray: obj must be an ImportData object')
    if not isinstance(res,(int,float)):
        raise TypeError('roundTimeArray: res must be a float or int')
    
    #round times to resolution and return to object array
    
    rounded_times = []
    for time in obj._time:
        minminus = datetime.timedelta(minutes = (time.minute % res))
        minplus = datetime.timedelta(minutes=res) - minminus
        if (time.minute % res) <= res/2:
            newtime = time - minminus
        else:
            newtime=time + minplus
    rounded_times.append(newtime)
    
    obj._time = rounded_times
    
    #remove duplicate times from the array
    
    unique_times = []
    unique_values = []
    for time in obj._time:
        if time not in unique_times:
            if repeat_operation == 'average':
                combined_value = np.average(obj.linear_search_value(time))
            if repeat_operation == 'sum':
                combined_value = np.sum(obj.linear_search_value(time))
                unique_times.append(time)
                unique_values.append(combined_value)
        else: 
            continue
    
    obj._time = unique_times
    obj._value = unique_values

    output = zip(obj._time,obj._value)

    return output
    
    
                
    

    # Inputs: obj (ImportData Object) and res (rounding resoultion)
    # objective:
    # create a list of datetime entries and associated values
    # with the times rounded to the nearest rounding resolution (res)
    # ensure no duplicated times
    # handle duplicated values for a single timestamp based on instructions in
    # the assignment
    # return: iterable zip object of the two lists
    # note: you can create additional variables to help with this task
    # which are not returned
    pass


def printArray(data_list, annotation_list, base_name, key_file):
    # combine and print on the key_file
    pass

if __name__ == '__main__':

    #adding arguments
    parser = argparse.ArgumentParser(description= 'A class to import, combine, and print data from a folder.',
    prog= 'dataImport')

    parser.add_argument('folder_name', type = str, help = 'Name of the folder')

    parser.add_argument('output_file', type=str, help = 'Name of Output file')

    parser.add_argument('sort_key', type = str, help = 'File to sort on')

    parser.add_argument('--number_of_files', type = int,
    help = "Number of Files", required = False)

    args = parser.parse_args()


    #pull all the folders in the file
    #files_lst = # list the folders


    #import all the files into a list of ImportData objects (in a loop!)
    data_lst = []

    #create two new lists of zip objects
    # do this in a loop, where you loop through the data_lst
    data_5 = [] # a list with time rounded to 5min
    data_15 = [] # a list with time rounded to 15min

    #print to a csv file
    #printLargeArray(data_5,files_lst,args.output_file+'_5',args.sort_key)
    #printLargeArray(data_15, files_lst,args.output_file+'_15',args.sort_key)
