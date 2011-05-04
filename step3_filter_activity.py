#!/usr/bin/python
"""
1. Detrend activity for each region (table row).
2. Denoise activity for each region.
3. Bandlimit the frequencies of activity for each region.

Re: bandpass filtering:
From: Susan Whitfield-Gabrieli <swg@mit.edu>
Date: Thu, Mar 10, 2011 at 10:10 AM
I'd recommend a band pass filter for resting scans with the low pass being < 0.1HZ.
Often people something like (0.004 < f < 0.08 Hz). There are a couple of papers
that discuss the influence of
1. when best to apply the bpf wrt other preprocessing steps
2. how the major action is in this range as opposed to higher freq (Salvadore)
From: Gael Varoquaux <gael.varoquaux@normalesup.org>
Date: Fri, Mar 11, 2011 at 6:15 AM
I'd use a band pass filter, cut above 0.1 Hz, and below half the acquisition length.

(c) Arno Klein  .  arno@binarybottle.com  .  2011  .  MIT license
"""

detrend = 1
denoise = 1
bandpass = 1

data_path = '/hd2/data/Brains/FunctionalConnectomes1000/NewYork_a_ADHD_part1/'
table_path = '/projects/homology/output/tables/'
table_end = '.csv'
table_end_filtered = '_filtered.csv'
label_column = 0 # 0-based
first_column = 1 # 0-based
out_image_path = './output/images/'

thresh_deviations = 5
TR = 2
freq_lower = 0.0
freq_upper = 0.10

import os
import numpy as np
import csv
import scipy
import matplotlib.pyplot as plt
from nitime.timeseries import TimeSeries
from nitime.analysis import FilterAnalyzer
import rpy2.robjects as robj
from detrendR import rdetrend
import warnings
warnings.simplefilter('ignore')

debug_run1 = 0
debug_plot = 0
save_figure = 0

if __name__ == '__main__':

    # Iterate over subjects
    for subject_id in os.listdir(data_path):

        table_file = table_path + subject_id + table_end
        out_filtered_file = table_path + subject_id + table_end_filtered
        print('Table: ' + table_file)

        try:

            # Import table and extract all non-empty rows (not incl. first column):
            table_reader = csv.reader(open(table_file,'r'), delimiter=',', quotechar='"')
            table = []
            labels = []
            for row in table_reader:
                table.append([np.float(s) for s in row if s!=''][first_column::])
                labels.append(np.int(np.float(row[label_column])))

            # Prepare output array:
            nrows = len(table)
            ncols = len(table[0])
            filtered = np.array(np.zeros((nrows,ncols+1)))

            if debug_plot:
                fig = plt.figure()
                ax = fig.add_subplot(111)

            # Iterate over rows (regions):
            for irow, row in enumerate(table):

                if debug_plot:
                    row_original = row

                """
                Detrend the activity for each region.
                """
                if detrend:
                   #row = scipy.signal.detrend(row, axis = 0, type = 'linear', bp = 0) # + 643
                    row_detrend = rdetrend(robj.FloatVector(row))
                    row = row_detrend

                """
                Denoise the activity for each region.
                """
                if denoise:
                    row_denoise = row
                    median_abs_deviation = np.median(np.abs(row_denoise - np.median(row_denoise)))
                    for ientry, entry in enumerate(row_denoise):
                        if abs(entry) > abs(thresh_deviations * median_abs_deviation):
                            if ientry > 0 and ientry < ncols-1:
                                row_denoise[ientry] = np.mean([row_denoise[ientry-1], row_denoise[ientry+1]])
                    row = row_denoise

                """
                Bandpass the frequencies of activity for each region.
                """
                if bandpass:
                    # Initialize a TimeSeries object:
                    T = TimeSeries(row,sampling_interval=TR)
                    row_bandpass = FilterAnalyzer(T,lb=freq_lower,ub=freq_upper).filtered_fourier
                    row = row_bandpass

                """
                Detrend activity a second time for each region.
                """
                detrend2 = 0
                if detrend2:
                   #row = scipy.signal.detrend(row, axis = 0, type = 'linear', bp = 0) # + 643
                    row_detrend2 = rdetrend(robj.FloatVector(row))
                    row = row_detrend2

                if debug_plot:
                    if detrend and denoise and bandpass:
                        ax.plot(range(0,ncols,1),row_original,'k+--',
                                range(0,ncols,1),row_detrend,'bo-',
                                range(0,ncols,1),row_denoise,'go-',
                                range(0,ncols,1),row_bandpass,'ro-')
                    else:
                        ax.plot(range(0,ncols,1),row_original,'k+--',range(0,ncols,1),row,'ko-')
                    plt.xlabel('Time points',fontsize='16')
                    plt.ylabel('Activity in region '+str(labels[irow])+' ('+str(freq_lower)+'-'+str(freq_upper)+'Hz)',fontsize='16')
                    plt.title('Activity: average(-), detrend(b), denoise(g), bandpass(r) (subject '+subject_id+')',fontsize='18')
                    # Save figure:
                    if save_figure:
                        fname = out_image_path + subject_id + '_filtered_activity.pdf'
                        plt.savefig(fname, dpi=None, facecolor='w', edgecolor='w',
                            orientation='landscape', papertype=None, format=None,
                            transparent=False, bbox_inches=None, pad_inches=0.0)

                label = np.array((np.float(labels[irow])))
                filtered[irow] = np.hstack((label,row))

            # Save the output to a text file:
            np.savetxt(out_filtered_file, filtered, delimiter=",")

        except IOError:
            raise

        if debug_run1:
            raise NameError('STOPPED')
