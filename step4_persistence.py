"""
Compute persistence and create a persistence diagram.

Much of this code was supplied by Dimitriy Morozov

"""

import sys, os
import csv
from glob import glob
import numpy as np
import pylab as plt
from itertools import combinations

base_path = '/projects/topology_2010/'
out_path = base_path + 'output/tables/'

plot_persistence_diagrams = 0
run_dionysus = 1
if run_dionysus:
  from dionysus import Simplex, DynamicPersistenceChains, Filtration, data_dim_cmp
  import time
kskeleton = 3  # A k-simplex has k+1 vertices
run_rips = 0  # Set to 1 to compute the Rips complex; else frequency filtration
if run_rips:
  import rips_pairwise_array
  #max_rips = 20
  in_table_path = base_path + 'output/tables/ROIxTR/'
  in_table_path_end = '_ROIvsTR.csv'
  out_path_end = '_persistence_diagram_Rips.csv'
else:
  in_table_path = base_path + 'output/tables/ROIxTR_binary/'
  in_table_path_end = '_ROIvsTR_binary.csv'
  in_file_path = base_path + 'output/tables/ROIxTR_binary_nconcurrences/'
  in_file_path_end = '_nconcurrences.txt'
  out_path_end1 = '_persistence' + str(kskeleton) + '_diagram_Freq.csv'
  out_path_end2 = '_persistence' + str(kskeleton) + '_data_Freq.csv'
first_column = 0 # 0-based
reverse_filtration_order = 1
set_filtration1_to_0 = 1

#Calculates the Binomial Coefficient
from math import factorial
def Binomial(n,k):
    if n > k:
        b = factorial(n) / (factorial(k)*factorial(n-k))
        return b

if __name__ == '__main__':
  """
  This program outputs 1 csv file per subject, 
  where each row is a voxel and columns are fMRI TRs.
  """
  # Iterate over subjects
  for table_file in glob(in_table_path + '*' + in_table_path_end):
    table_id = table_file.split('/')[-1].split('.')[0]
    print('Table: ' + table_file)
    if 1==1:
    #if os.path.exists(out_file):
    #  pass
    #else:

      #################
      # Prepare table #
      #################
      # Import table: 
      table_reader = csv.reader(open(table_file,'r'), delimiter=',', quotechar='"')
        
      # Extract all non-empty rows for columns greater than first_column:
      table = []
      for irow, row0 in enumerate(table_reader):
        table.append([np.float(s2) for s2 in row0 if s2!=''][first_column:-1])

      # Count:
      nrows = len(table)
      ncols = len(table[0])
      print('k-skeleton = ' + str(kskeleton))
      print('Number of columns = ' + str(ncols))
      print('Number of rows = ' + str(nrows))

      # Convert the table list to a table array:
      table_array = np.array(np.zeros((nrows,ncols)))
      for irow, row in enumerate(table):
        table_array[irow] = table[irow]

      # Import file: 
      if run_rips: 
        pass
      else:
        # Load frequency filtration numbers:        
        num_file = in_file_path + table_id + in_file_path_end
        print('File: ' + num_file)
        nconcurrences = np.loadtxt(num_file)
        if set_filtration1_to_0:
          nconcurrences = nconcurrences - 1
        # Convert number of concurrences to filtration order (max is time 0):
        # FIX!
        if reverse_filtration_order:
          max_nconcurrences = max(nconcurrences)
          print('Maximum number of concurrences = ' + str(max_nconcurrences))
          nfiltrations = max_nconcurrences - nconcurrences
        else:
          nfiltrations = nconcurrences
          max_nconcurrences = max(nfiltrations)
          print('Maximum number of concurrences = ' + str(max_nconcurrences))
        
      ###############
      # Persistence #
      ###############
      if run_dionysus:
        print('Dionysus software for persistence homology...')
        if run_rips:
          out_file = out_path + table_id + out_path_end
          max_rips = len(table_array[0])*np.mean(table_array.ravel())
          rips_pairwise_array.main(table, kskeleton, max_rips, out_file1, plot_persistence_diagrams)
        else:
          # Create simplices
          print('Construct simplices...')
          simplices = Filtration()
          for icol in range(ncols):
            inon0 = np.nonzero(table_array[:,icol]==1)[0]
            if len(inon0) > 0:
              simplex_column = Simplex([int(s) for s in inon0]) 
              # Include all faces in each simplex
              # Compute the k-skeleton of the closure of the list of simplices.
              # A k-simplex has k+1 vertices.
              for k in range(1, np.min([kskeleton+2,simplex_column.dimension()+1])):
                for face in combinations(simplex_column.vertices, k):
                  simplex_face = Simplex(face)
                  """
                  You can call a filtration with a simplex, 
                  and it will tell you its index in the filtration.
                  So if s is Simplex() and f a Filtration(), then
                  f(s) returns the index of s in the filtration.
                  """
                  i = simplices(simplex_face)
                  if i < len(simplices):
                    existing_data = simplices[i].data
                    simplices[i].data = min(existing_data, nfiltrations[icol])
                  else:
                    simplex_face.data = nfiltrations[icol]
                    simplices.append(simplex_face)

          nsimplices = simplices.__len__()
          print('Number of faces computed: ' + str(nsimplices)) 
          
          # Sort simplicessimplices.__len__()
          print('Sort simplices...')
          simplices.sort(data_dim_cmp)
          print(time.asctime())
          print("Set up filtration")

          p = DynamicPersistenceChains(simplices)
          print(time.asctime())
          print("Initialized DynamicPersistenceChains")
            
          p.pair_simplices()
          print(time.asctime())
          print("Simplices paired")
            
          print("Output persistence")
          out_file1 = out_path + table_id + out_path_end1
          out_file2 = out_path + table_id + out_path_end2
          if plot_persistence_diagrams:
            f1 = open(out_file1,"w")
          f2 = open(out_file2,"w")
          smap = p.make_simplex_map(simplices)

          """
          Dimitriy Morozov: 
          Each row describes its own homology class, 
          but only at a certain time in the filtration. 
          So, for example, if a cycle z = <...> <...> is given in row 
          with birth, death = 10, 11, it means that that cycle was new 
          (as in not the image of anything from before and not trivial) 
          at time 10. At time 11, however, it became homologous to 0, 
          i.e. a trivial cycle (i.e. a boundary). Now, of course, 
          if by time 15 a number of cycles die, then they are all trivial 
          and homologous to each other. Moreover adding them to any 
          alive cycle won't change its homology class (adding 0 to 
          anything doesn't change it).
          When you see cycles in rows with persistence 0, you can safely
          ignore them. They simply are artifacts of the fact that we have 
          to process the filtration one simplex at a time. So from the 
          algorithm's point of view a number of things happened at time "11", 
          and a number of complexes existed (some giving births, 
          some giving deaths). But from our point of view, all that matters 
          is what happens at the end of step 11, which means that everything 
          that was born and died at 11 is homologous to 0, and can and should 
          be ignored.
          DynamicPersistenceChains stores full cycles (both positive and 
          negative simplices). It also stores what I call chains. 
          These allow you to get at the cycles that never die.
          """
          for i in p:
              if not i.sign():  continue
              birth = smap[i]
              if i.unpaired():
                cycle = i.chain
                death_value = "inf"
              else:
                cycle = i.pair().cycle
                death_value = smap[i.pair()].data
              #sys.exit()
              #print(birth.data,death_value)
              if birth.data > 0 and birth.data != death_value and birth.data != max_nconcurrences and death_value != max_nconcurrences:
                smap_str = ''
                for ii in cycle: 
                  smap_str = smap_str + " " + str(smap[ii])
                ddate = death_value
                #if reverse_filtration_order:
                #  bdate = max_nconcurrences - birth.data
                #  if not i.unpaired():
                #    ddate = max_nconcurrences - death_value
                #else:
                bdate = birth.data
                s0 = [str(birth.dimension()),str(bdate),str(ddate)]
                s1 = " ".join(s0)
                s2 = " ".join([s1,smap_str])
                #s3 = " ".join(["Dim, t0, t1, cycles:",s2])
                #print(s3)
                if plot_persistence_diagrams:
                  f1.writelines(" ".join([s1,"\n"]))
                f2.writelines(" ".join([s2,"\n"]))
          f2.close()
          if plot_persistence_diagrams:
              f1.close()
              cmd = 'python draw.py ' + out_file1
              print(cmd); os.system(cmd)
