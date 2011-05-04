#!/usr/bin/python
"""
Run frequency filtration on a binary table.

Filter the table by the number of times (frequency) that the active regions 
of a given column are repeated as a subset of the active regions of the other columns.
The complex at frequency level f includes all concurrences that happen at least f times.

(c) Arno Klein  .  arno@binarybottle.com  .  2011  .  MIT license
"""

filter_by_frequency = 1

data_path = '/hd2/data/Brains/FunctionalConnectomes1000/NewYork_a_ADHD_part1/'
table_path = '/projects/homology/output/tables/'
table_end = '_binary.csv'
nconcurrences_file_end = '_nconcurrences.txt'
nregions_per_concurrence_file_end = '_nregions_per_concurrence.txt'
first_column = 1 # 0-based

import sys, os
import csv
import numpy as np
import pylab as plt

debug_run1 = 0
debug_plot = 0

if __name__ == '__main__':

    # Iterate over subjects
    for subject_id in os.listdir(data_path):

        table_file = table_path + subject_id + table_end
        nconcurrences_file = table_path + subject_id + nconcurrences_file_end
        nregions_per_concurrence_file = table_path + subject_id + nregions_per_concurrence_file_end
        print('Table: ' + table_file)

        try:

            """
            Import table and extract all non-empty rows (not incl. first column).
            """
            table_reader = csv.reader(open(table_file,'r'), delimiter=',', quotechar='"')
            [nrows,ncols] = np.shape([s for s in table_reader])
            ncols = ncols - 1
            print('Number of columns = ' + str(ncols))
            print('Number of rows = ' + str(nrows))
            table = np.zeros((nrows,ncols))
            table_reader = csv.reader(open(table_file,'r'), delimiter=',', quotechar='"')
            for irow, row in enumerate(table_reader):
                table[irow] = [np.int(np.float(s)) for s in row if s!=''][first_column::]

            """
            FREQUENCY FILTRATION:
            Filter the table by the number of times (frequency) that the active regions 
            of a given column are repeated as a subset of the active regions of the other columns.
            The complex at frequency level f includes all concurrences that happen at least f times.
            """
            if filter_by_frequency:
                nconcurrences = np.zeros(ncols, dtype=int)
                nregions = np.zeros(ncols, dtype=int)
                for icol1 in range(ncols):
                    i1 = np.nonzero(table[:,icol1]==1)[0]
                    if len(i1) > 0:
                        nconcurrences[icol1] += 1
                        nregions[icol1] = len(i1)
                        for icol2 in range(ncols):
                            if icol2 != icol1:
                                i2 = np.nonzero(table[:,icol2]==1)[0]
                                if len(np.intersect1d(i1,i2)) == len(i1):
                                    nconcurrences[icol1] += 1
                max_nconcurrences = np.max(nconcurrences)
                print('Maximum number of concurrences = ' + str(max_nconcurrences))
                # Save the number of concurrences in a text file:
                np.savetxt(nconcurrences_file, nconcurrences)
                np.savetxt(nregions_per_concurrence_file, nregions)

            # Plot:
            if debug_plot and filter_by_frequency:
                fig = plt.figure(facecolor='white')
                ax = fig.add_subplot(111, autoscale_on=False, xlim=(0,ncols), ylim=(0,max_nconcurrences+1))
                ax.plot(range(0,ncols,1), nconcurrences, 'k-')
                ax.scatter(range(0,ncols,1), nconcurrences, marker='o', s=nregions)
                plt.xlabel('Time points',fontsize='16')
                plt.ylabel('Number of concurrences',fontsize='16')
                plt.title('Number of concurrences (radius = #regions; subject '+subject_id+')',fontsize='18')

        except IOError:
            raise

        if debug_run1:
            raise NameError('STOPPED')
