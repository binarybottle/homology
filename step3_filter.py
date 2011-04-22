"""
Run frequency filtration on a binary table.

Filter the table by the number of times (frequency) that the active regions 
of a given column are repeated as a subset of the active regions of the other columns.
The complex at frequency level f includes all concurrences that happen at least f times.

(c) Arno Klein  .  arno@binarybottle.com  .  2011
"""

import sys, os
import csv
from glob import glob
import numpy as np
import pylab as plt

from settings import binary_table_path, binary_table_path2, binary_table_end, binary_table_end2, first_column

filter_by_frequency = 1
save_tables = 1
plot_figure = 0
if plot_figure:
  colorbar = 1
  save_figure = 0

if __name__ == '__main__':
    """
    This program outputs one csv file per subject, 
    where each row is a voxel and columns are fMRI TRs.
    """
    # Iterate over subjects
    for table_file in glob(binary_table_path + '*' + binary_table_end):
      table_id = table_file.split('/')[-1].split('.')[0]
      print('Table: ' + table_file)

      out_file = binary_table_path2 + table_id + binary_table_end2
      if os.path.exists(out_file):
        pass
      else:

        #################
        # Prepare table #
        #################
        # Import table:
        table_reader = csv.reader(open(table_file,'r'), delimiter=',', quotechar='"')
        #fh = open(table_file,'r'); table_reader = fh.readlines()

        # Extract all non-empty rows for columns to the right of the first_column:
        table = []
        for irow, row0 in enumerate(table_reader):
          table.append([np.float(s2) for s2 in row0 if s2!=''][first_column:-1])

        # Count:
        nrows = len(table)
        ncols = len(table[0])
        print('Number of columns = ' + str(ncols))
        print('Number of rows = ' + str(nrows))

        # Convert the table list to a table array:
        table_array_bin = np.array(np.zeros((nrows,ncols)))
        for irow, row in enumerate(table):
            table_array_bin[irow] = table[irow]

        ########################
        # FREQUENCY FILTRATION #
        ########################
        # Filter the table by the number of times (frequency) that the active regions 
        # of a given column are repeated as a subset of the active regions of the other columns.
        # The complex at frequency level f includes all concurrences that happen at least f times.
        if filter_by_frequency:

          nconcurrences = np.zeros(ncols)
          for icol1 in range(ncols):
            i1 = np.nonzero(table_array_bin[:,icol1]==1)[0]
            if len(i1) > 0:
              nconcurrences[icol1] += 1
              for icol2 in range(ncols):
                if icol2 != icol1:
                  i2 = np.nonzero(table_array_bin[:,icol2]==1)[0]
                  if len(np.intersect1d(i1,i2)) == len(i1):
                    nconcurrences[icol1] += 1
          max_nconcurrences = np.max(nconcurrences)
          print('Maximum number of concurrences = ' + str(max_nconcurrences))

          """
          # Frequency filtration:
          print('Frequency filtration...')
          frequency_table = table_array_bin * nconcurrences
          frequency_tables = np.zeros((nrows,ncols,max_nconcurrences))
          for ifilter in range(max_nconcurrences):
            i,j = np.nonzero(frequency_table > ifilter)
            frequency_tables[i,j,ifilter] = 1
          """

          # Save:
          if save_tables:
            np.savetxt(out_file, nconcurrences)

        ########
        # Plot #
        ########
        if plot_figure:
          for ifilter in range(max_nconcurrences):
            fig = plt.figure(facecolor='white')
            ax = fig.add_subplot(111, autoscale_on=False, xlim=(0,ncols), ylim=(0,nrows))
            ftable = frequency_tables[:,:,ifilter]
            p3 = ax.pcolor(ftable)

