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

    data_frame = import_data(filename)
    data_frame['time'] = pd.to_datetime(data_frame['time'])
    data_frame = data_frame.set_index('time')
    data_frame = data_frame[data_frame['value'].apply(type) != str]
    data_frame['value'].astype(float)
    new_title = get_title(filename)
    data_frame = data_frame.rename(columns = {'value' : new_title})
    return data_frame


def get_title(filename):
    sep1 = '/'
    sep2 = '_'
    text = filename.split(sep1,2)[1]
    text = text.split(sep2,1)[0]
    return text

def main():
    data_frames = []
    for filename in os.listdir('smallData'):

        filepath = 'smallData/'+filename
        data_frames.append(format_data(filepath))

    df_key = data_frames[3]
    del data_frames[3]
    df = df_key.join(data_frames)
    df=df.fillna(0)
    df['time5'] = df.index.round('5min')
    df['time15'] = df.index.round('15min')
    
    df_5 = df.set_index('5min')
    df_15 = df.set_index('15min')
    
    
    return df,df_5,df_15
        
    



if __name__ == '__main__':
    df,dfs = main()
