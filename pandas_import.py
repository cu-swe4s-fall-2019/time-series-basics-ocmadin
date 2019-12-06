import numpy as np
import pandas as pd
import datetime as dt
import os

def import_data(filepath):
    if not isinstance(filepath,str):
        raise TypeError('import_data: filepath must be a string')

    if filepath.endswith('.csv'):
        data_frame = pd.read_csv(filepath)
        return data_frame
    
    else:
        raise ImportError('import_data: filepath string must be csv')

def format_data(filename):
    filepath = 'smallData/'+filename
    data_frame = import_data(filepath)
    data_frame['time'] = pd.to_datetime(data_frame['time'])
    data_frame = data_frame.set_index('time')
    data_frame['value'].astype(float)
    return data_frame

        
def main():
    for filename in os.listdir('smallData'):
        data_frame = import_data(filename)
        data_frame = format_data(data_frame)
    return data_frame
        
    



if __name__ == '__main__':
    data_frame = main()
