import matplotlib.pyplot as plt
from io import StringIO
import pandas as pd
import numpy as np

def get_digit_dataframe(filename):
    # write string with every character except degree sign
    # return pandas data frame from file
    with open(filename, 'rb') as f:
        ba = f.read()
        outstring = ''
        for b in ba:
            if b != ord(b'\xb0'):
                outstring += chr(b)
    return pd.read_csv(StringIO(outstring), parse_dates=True, index_col=0)


def combine_data(filename_inside, filename_outside, filename_output):

    # read data
    data_in = get_digit_dataframe(filename_inside)
    data_out = get_digit_dataframe(filename_outside)

    # resample
    data_in_resamp = data_in.resample('5T').pad()
    data_out_resamp = data_out.resample('5T').pad()

    # merge data
    final_data = pd.merge(data_in_resamp,
                          data_out_resamp,
                          left_index=True,
                          right_index=True,
                          how='inner')

    # clean up column names
    final_data['t_in'] = final_data['Temperature (C)_x']
    final_data['t_out'] = final_data['Temperature (C)_y']

    # drop blank data
    final_data.dropna(inplace=True)

    #print(final_data.head())
    # get second time samples
    final_data['time'] = final_data['Time.1_x'] - final_data['Time.1_x'][0]

    final_data = final_data[['time', 't_in', 't_out']]

    final_data.to_csv(filename_output)

    # return to caller
    return final_data
    # make units obvious?
    # write to csv
    # return dataframe (for debugging or whatever)

