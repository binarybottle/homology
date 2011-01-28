"""
Remove rows with variation less than a minimum range of variation.
Binarize the remaining rows according to a threshold.

"""

import sys, os
import csv
from glob import glob
import numpy as np
import pylab as plt
from percentile import percentile

# Paths
base_path = '/projects/topology_2010/'
out_image_path = base_path + 'output/images/'
in_table_path = base_path + 'output/tables/ROIxTR/'
in_table_path_end = 'ROIvsTR.csv'
first_column = 1 # 0-based
out_table_path = base_path + 'output/tables/ROIxTR_binary/'

min_percentile = 0  # Set to 0 if retain all rows (regions); else, e.g. 0.25
thresh_nstds = 2  # Set >0 to threshold table by thresh_nstds SDs above a row's mean
save_tables = 1
plot_figure = 0
if plot_figure:
  colorbar = 1
  save_figure = 0

"""
# http://stackoverflow.com/questions/1159524/how-to-replace-a-column-in-a-csv-file-in-python
def transpose(matrix):
    return [[matrix[x][y] for x in range(len(matrix))] for y in range(len(matrix[0]))]

# from mstats.py, after idealfourths
def interquartile_range(data): 
  \"""Returns an estimate of the interquartile range of the data, 
     as computed with the ideal fourths.
  \"""
  data = np.ma.masked_array(data, copy=False)
  x = np.sort(data.compressed())
  n = len(x)
  (j, h) = divmod(n / 4. + 5 / 12., 1)
  qlo = (1 - h) * x[j] + h * x[j + 1]
  k = n - j
  qup = (1 - h) * x[k] + h * x[k - 1]
  return qup - qlo
  
def variation_range(data, axis_arg=None):  
  #return interquartile_range(data)
  #return np.std(data)/np.mean(data)
  return np.std(data, axis=axis_arg)
"""

if __name__ == '__main__':
    """
    This program outputs 1 csv file per subject, 
    where each row is a voxel and columns are fMRI TRs.
    """
    # Iterate over subjects
    for table_file in glob(in_table_path + '*' + in_table_path_end):
      table_id = table_file.split('/')[-1].split('.')[0]
      print('Table: ' + table_file)

      out_file1 = out_table_path + table_id + '_variable.csv'
      out_file2 = out_table_path + table_id + '_binary.csv'
      if os.path.exists(out_file1) or os.path.exists(out_file2):
        pass
      else:

        #################
        # Prepare table #
        #################
        # Import table: 
        table_reader = csv.reader(open(table_file,'r'), delimiter=',', quotechar='"')
        #fh = open(table_file,'r'); table_reader = fh.readlines()        

        # Extract all non-empty rows for columns greater than first_column:
        table = []
        for irow, row0 in enumerate(table_reader):
          table.append([np.float(s2) for s2 in row0 if s2!=''][first_column:-1])

        ##print(table)          
        ##table = transpose(table)
        ##plt.hist(np.ravel(table))
        ##plt.hist(np.std(table,axis=1),bins=100)
        
        # Count:
        print('Number of columns = ' + str(len(table[0])))
        print('Number of rows = ' + str(len(table)))

        # Remove rows with variation less than a minimum range of variation:
        if min_percentile > 0:
          stds = np.std(table, axis=1)
          std_thresh = percentile(list(np.sort(stds)), min_percentile)
          irows = np.nonzero(stds >= std_thresh)[0]
          table_variable = []
          for irow1 in irows:
            table_variable.append(table[irow1]) 
          table = table_variable
          # Save:
          if save_tables:
            np.savetxt(out_file1, table_array, delimiter=",")

        # Count:
        nrows = len(table)
        ncols = len(table[0])
        voxel_ids = range(nrows)
        if min_percentile > 0:
          print('Number of rows above threshold of variation = ' + str(nrows))
               
        # Binarize table:
        if thresh_nstds > 0:
          # Convert the table list to a table array:
          table_array = np.array(np.zeros((nrows,ncols)))
          for irow, row in enumerate(table):
            table_array[irow] = table[irow]
          # Threshold:
          table_array_bin = np.zeros(np.shape(table_array))
          for irow, row in enumerate(table_array):
            #table_array_bin[irow][np.nonzero(row >= np.mean(row))] = 1
            table_array_bin[irow][np.nonzero(row >= np.mean(row) + thresh_nstds * np.std(row))] = 1
            table_array_bin[irow][np.nonzero(row <= np.mean(row) - thresh_nstds * np.std(row))] = 1        

          print("Sum of binary table entries: " + str(np.sum(table_array_bin.ravel())))

          # Save:
          if save_tables:
            np.savetxt(out_file2, table_array_bin, delimiter=",")


        ########
        # Plot #
        ########
        if plot_figure and thresh_nstds > 0:
          fig = plt.figure(facecolor='white')
          # Subplot 1:
          ax = fig.add_subplot(211, autoscale_on=False, xlim=(0,ncols), ylim=(0,nrows))
          colormap = 'gist_heat'
          plt.set_cmap(colormap)
          p1 = ax.pcolor(table_array)
          plt.ylabel('Regions',fontsize='18')
          plt.title('BOLD activity for regions with SD/mean > '+str(max_coeff_of_var)[0:4],fontsize='18')
          plt.yticks(np.arange(1,nrows+1)-0.5,voxel_ids)
          # Colorbar:
          if colorbar:
            cbar = fig.colorbar(p1)
        
          # Subplot 2:
          ax = fig.add_subplot(212, autoscale_on=False, xlim=(0,ncols), ylim=(0,nrows))
          colormap = 'gray'
          plt.set_cmap(colormap)
          p2 = ax.pcolor(table_array_bin)
          plt.xlabel('TR',fontsize='18')
          plt.ylabel('Regions',fontsize='18')
          plt.title('Threshold per region: mean+SD (colored by frequency)',fontsize='18')
          plt.yticks(np.arange(1,nrows+1)-0.5,voxel_ids)
          # Colorbar:
          if colorbar:
            cbar = fig.colorbar(p2)
          # Save figure:
          if save_figure:
            fname = out_image_path + table_id + '_VOXxTR.pdf'
            plt.savefig(fname, dpi=None, facecolor='w', edgecolor='w',
                    orientation='landscape', papertype=None, format=None,
                    transparent=False, bbox_inches=None, pad_inches=0.0)

