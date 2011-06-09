#!/usr/bin/python
"""
1. Remove rows of a table file with least variation (interquartile range over median).
2. Binarize the remaining rows, with a 1 indicating high activity.

(c) Arno Klein  .  arno@binarybottle.com  .  2011  .  MIT license
"""

min_percentile_variation = 20
min_percentile_activity = 80

data_path = '/hd2/data/Brains/FunctionalConnectomes1000/NewYork_a_ADHD_part1/'
table_path = '/projects/homology/output/tables/'
table_end = '_filtered.csv'
table_end_binary = '_binary.csv'

import sys, os
import csv
import numpy as np
import pylab as plt
from scipy.stats import scoreatpercentile

# Paths
out_image_path = './output/images/'
label_column = 0 # 0-based
first_column = 1 # 0-based

debug_run1 = 1
debug_plot = 0
save_figure = 0

if __name__ == '__main__':

    # Iterate over subjects:
    for subject_id in os.listdir(data_path):

        table_file = table_path + subject_id + table_end
        out_binary_file = table_path + subject_id + table_end_binary
        print('Input and output tables: ' + table_file + ', ' + out_binary_file)

        try:

            """
            Import table and extract all non-empty rows (not incl. first column).
            """
            table_reader = csv.reader(open(table_file,'r'), delimiter=',', quotechar='"')
            table = []
            labels = []
            for row in table_reader:
                table.append([np.float(s) for s in row if s!=''][first_column::])
                labels.append(row[label_column])

            """
            Remove rows with variation less than a minimum range of variation (interquartile range over median).
            """
            if min_percentile_variation:
                IQRs_over_medians = np.zeros(len(table))
                for irow, row in enumerate(table):
                    try:
                        IQRs_over_medians[irow] = (scoreatpercentile(row,75) - scoreatpercentile(row,25))/np.median(row)
                    except:
                        pass
                IQR_thresh = scoreatpercentile(IQRs_over_medians, min_percentile_variation)
                irows = np.nonzero(IQRs_over_medians >= IQR_thresh)[0]
                table_variable = []
                labels_variable = []
                for irow in irows:
                    table_variable.append(table[irow]) 
                    labels_variable.append(labels[irow]) 
                table = table_variable
                labels = labels_variable
                print('Number of rows above threshold of variation = ' + str(len(labels)) + ' of ' + str(len(table)))

            # Count:
            nrows = len(table)
            ncols = len(table[0])

            """
            Binarize table.
            """
            if min_percentile_activity:
                table_binary = np.array(np.zeros((nrows,ncols+1)))
                for irow, row in enumerate(table):
                    row_thresh = scoreatpercentile(row, min_percentile_activity)
                    ientries = np.nonzero(row >= row_thresh)[0] + 1
                    #print('Number of columns above threshold of activity = ' + str(len(ientries)) + ' of ' + str(ncols))
                    table_binary[irow][0] = np.array((np.float(labels[irow])))
                    table_binary[irow][ientries] = 1
                    #print('Sum of columns above threshold of activity = ' + str(np.sum(table_binary[irow][1::])) + ' of ' + str(ncols))
                # Save binary table:
                np.savetxt(out_binary_file, table_binary, delimiter=",")

            # Plot:
            if debug_plot and min_percentile_activity:
                fig = plt.figure(facecolor='white')
                ax = fig.add_subplot(111, autoscale_on=False, xlim=(0,ncols), ylim=(0,nrows))
                #colormap = 'gray'
                #plt.set_cmap(colormap)
                plt.xlabel('Time points',fontsize='16')
                plt.ylabel('Regions',fontsize='16')
                plt.title('Top '+str(100-min_percentile_activity)+'% activity for regions with top '+str(100-min_percentile_variation)+'% variation (subject '+subject_id+')',fontsize='18')
                plt.yticks(np.arange(1,nrows+1)-0.5,[np.int(np.float(s)) for s in labels])
                p2 = ax.pcolor(table_binary[::,1::]/np.max(table_binary[::,1::]))
                # Save figure:
                if save_figure:
                    fname = out_image_path + subject_id + '_binary_activity.pdf'
                    plt.savefig(fname, dpi=None, facecolor='w', edgecolor='w',
                        orientation='landscape', papertype=None, format=None,
                        transparent=False, bbox_inches=None, pad_inches=0.0)

        except IOError:
            raise

        if debug_run1:
            raise NameError('STOPPED')
