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
                        self._value.append(float(40))
                        print('ImportData: Replacing "low" value with 40')
                    elif row['value'] == 'high':
                        self._value.append(float(300))
                        print('ImportData: Replacing "high" value with 300')
                    else:
                        try:
                            self._value.append(float(row['value']))
                        except ValueError:
                            continue
                else:
                    if row['value'] == '':
                        print('ImportData: Removing blank value')
                        continue
                    try:
                        self._value.append(float(row['value']))
                    except ValueError:
                        continue
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



def printArray(data_list, annotation_list, base_name, key_file):
    
    if data_list is None:
        raise TypeError('printArray: requires data_list')
    if annotation_list is None:
        raise TypeError('printArray: requires annotation_list')
    if base_name is None:
        raise TypeError('printArray: requires base_name')
    if key_file is None:
        raise TypeError('printArray: requires key_file')
    if not isinstance(data_list,list):
        raise TypeError('printArray: data_list must be list')
    if not isinstance(annotation_list,list):
        raise TypeError('printArray: annotation_list must be list')
    if not isinstance(base_name,str):
        raise TypeError('printArray: base_name must be str')
    if not isinstance(key_file,str):
        raise TypeError('printArray: key_file must be str')
        

    
    for i in range(len(annotation_list)):
        if key_file == 'smallData/'+annotation_list[i]:
            align_data = data_list[i]
            key_index = i
            break

    if '.csv' not in base_name:
        raise TypeError('printArray: base_name must end with .csv')

    with open(base_name, 'w') as f:
        f.write('time'+annotation_list[key_index].split('/')[-1].split('_')[0]+',')
        other_files = list(range(len(annotation_list)))
        other_files.remove(key_index)
        
        for i in other_files:
            f.write(annotation_list[i].split('/')[-1].split('_')[0]+',')
        f.write('\n')
        
        for time, value in align_data:
            print('NO')
            f.write(str(time)+','+str(value)+',')
            for i in other_files:
                time_list = [data[0] for data in data_list[i]]
                if time in time_list:
                    f.write(str(data_list[i][time_list.index(time)][1])+',')
                else: f.write('0,')
            f.write('\n')
            

if __name__ == '__main__':

    #adding arguments
    parser = argparse.ArgumentParser(description= 'A class to import, combine, and print data from a folder.',
    prog= 'dataImport')

    parser.add_argument('--folder_name', type = str, help = 'Name of the folder')

    parser.add_argument('--output_file', type=str, help = 'Name of Output file')

    parser.add_argument('--sort_key', type = str, help = 'File to sort on')

    parser.add_argument('--number_of_files', type = int,
    help = "Number of Files", required = False)

    args = parser.parse_args()


    #pull all the folders in the file
    files_lst = [file for file in listdir(args.folder_name)] # list the folders
    #import all the files into a list of ImportData objects (in a loop!)
    data_lst = []
    
    for file in files_lst:
        data_lst.append([file,ImportData(args.folder_name+'/'+file)])
        
    #create two new lists of zip objects
    # do this in a loop, where you loop through the data_lst

    data_5 = [] # a list with time rounded to 5min
    data_15 = [] # a list with time rounded to 15min
    
    for data in data_lst:
        if data[0] == 'activity_small.csv':
            repeat_operation='sum'
        elif data[0] == 'bolus_small.csv':
            repeat_operation='sum'
        elif data[0] == 'meal_small.csv':
            repeat_operation='sum'
        else:
            repeat_operation = 'average'
        data_5.append(roundTimeArray(data[1],5,repeat_operation))
        data_15.append(roundTimeArray(data[1],15,repeat_operation))

    #print to a csv file
    printArray(data_5,files_lst,'5'+args.output_file,args.sort_key)
    printArray(data_15, files_lst,'15'+args.output_file,args.sort_key)