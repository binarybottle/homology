"""
Compute persistence and create a persistence diagram
from a binary table of activity data.

Much of this code was supplied by Dimitriy Morozov

(c) Arno Klein  .  arno@binarybottle.com  .  2010
"""

import sys, os
import csv
import numpy as np
import pylab as plt
from itertools import combinations
import time
from glob import glob

from dionysus import Simplex, data_dim_cmp, dim_data_cmp, closure,
                     Filtration, StaticPersistence, DynamicPersistenceChains

from settings import binary_table_path, binary_table_path2, binary_table_end, binary_table_end2

out_path = './output/tables/'

plot_persistence_diagrams = 0
kskeleton = 3  # A k-simplex has k+1 vertices
first_column = 0 # 0-based
reverse_filtration_order = 1
set_filtration1_to_0 = 1
dynamic_persistence = 1

# Calculate the binomial coefficient
from math import factorial
def Binomial(n,k):
    if n > k:
        b = factorial(n) / (factorial(k)*factorial(n-k))
        return b


if __name__ == '__main__':
    
  # Iterate over subjects
  for table_file in glob(binary_table_path + '*' + binary_table_end):
    table_id = table_file.split('/')[-1].split('.')[0]
    print('Load binary activity table: ' + table_file)
    if 1==1:
    #if os.path.exists(out_file):
    #  pass
    #else:

      # Import table 
      table_reader = csv.reader(open(table_file,'r'), delimiter=',', quotechar='"')
        
      # Extract all non-empty columns after the first_column
      table = []
      for irow, row in enumerate(table_reader):
        table.append([np.float(s) for s in row if s!=''][first_column:-1])
      print(' ' + str(len(table)) + ' regions, ' + \
            str(len(table[0])) + ' times')

      # Transpose table and create a new list of lists of indices 
      # for each original table column
      table_indices = []
      for col in np.transpose(table).tolist():
        icol = np.nonzero(col)
        table_indices.append([s for s in icol[0]])

      # Load frequency filtration numbers        
      num_file = binary_table_path2 + table_id + binary_table_end2
      print('Load filtration file: ' + num_file)
      nconcurrences = np.loadtxt(num_file)
      if set_filtration1_to_0:
        nconcurrences = nconcurrences - 1
        
      # Convert number of concurrences to filtration order (max is time 0):
      if reverse_filtration_order:
        max_nconcurrences = max(nconcurrences)
        nfiltrations = max_nconcurrences - nconcurrences
      else:
        nfiltrations = nconcurrences
        max_nconcurrences = max(nfiltrations)
      print(' Maximum number of concurrences = ' + str(max_nconcurrences))
      print(time.asctime())
      
      ###############
      # Persistence #
      ###############
      print('--- Dionysus software for persistence homology ---')
      
      # Create simplices
      print('Construct and sort simplices...')
      levels = []
      for itime, data_time in enumerate(table_indices):
        levels.append(Simplex([int(s) for s in data_time], itime))
      
      # Sort the list by data
      levels.sort(key = lambda s: s.data)
      print(time.asctime())
      
      # Include all faces in each simplex
      # Compute the k-skeleton of the closure of the list of simplices.
      # A k-simplex has k+1 vertices.
      print("Compute all " + str(kskeleton) + "-skeleton faces for each simplex...")
      complex = closure(levels, kskeleton+1)
      print(str(complex.__len__()) + ' faces computed') 
      print(time.asctime())

      print("Apply Filtration")      
      f = Filtration(complex, dim_data_cmp)
      #print("Complex in the filtration order:" + ', '.join((str(s) for s in f)))
      print(time.asctime())
      
      if dynamic_persistence == 0:
          """
          ######################
          # Static persistence #
          ######################
          StaticPersistence doesn't give you anything that 
          DynamicPersistenceChains wouldn't, only speed and memory advantage. 
          SP keeps track of strictly less information.
          Dmitriy Morozov's explanation of Dionysus's Triangle example:
            The output goes over all the simplices in the filtration order.
            > True True
            Sign of the simplex (True = positive, it creates a cycle; False =
            negative, it destroys a cycle), the second is the sign of the simplex
            paired with this simplex. By convention, an unpaired simplex is paired
            with itself, so it's the only time you can see True True
            A homology class is created after a simplex sigma enters a filtration
            (a representative cycle necessarily contains sigma). It is destroyed
            after tau enters a filtration, the chain that has that cycle as a
            boundary necessarily contains tau. We say that sigma and tau are a
            simplex pair.
            > <0> (1) - <0> (1)
            Simplex <0> is paired with itself, meaning that it's unpaired. The
            cycle it creates never gets killed. (The numbers in parentheses are
            redundant -- they are 1 if the simplex is positive, 0 if it's
            negative; so same information as the previous line.)
            > Cycle (0):
            If a simplex kills a cycle, that cycle is output on this line.
            > True False
            > <1> (1) - <0, 1> 2.500000 (0)
            > Cycle (0):
            <1> is a positive simplex, paired with a negative simplex <0, 1>. So a
            class that <1> created survived until <0, 1> appeared in the
            filtration. Since <1> is positive, the cycle is empty.
            That cycle field is non-empty only for negative simplices. It's
            the cycle that's destroyed when the negative simplex (tau, above)
            enters the filtration. A positive simplex entering the filtration does
            not kill any cycles, so the cycle field is necessarily empty.> False True
            > <0, 1> 2.500000 (0) - <1> (1)
            > Cycle (2): <1> + <0>
            <0, 1> is a negative simplex, paired with <1>. A representative cycle
            that it destroyed is <1> + <0>.
            > False True
            > <1, 2> 2.900000 (0) - <2> (1)
            > Cycle (2): <2> + <1>
            <1, 2> is negative, paired with <2>. <2> + <1> is a representative
            cycle that got killed.
            > False True
            > <0, 1, 2> (0) - <0, 2> 3.500000 (1)
            > Cycle (1): <0, 2> 3.500000
            <0, 1, 2> is a negative simplex, it killed a cycle created by <0,2>.
            Note that the representative cycle lists only the positive simplices.
            I.e. <0,2> by itself is not actually a cycle, but the cycle includes
            some negative simplices (in this case <0,1> and <1,2>) that are not
            listed in the output.
          """
          print("Initialize persistence...")
          p = StaticPersistence(f)
    
          print("Pair simplices...")
          p.pair_simplices()
          print(time.asctime())
          
          smap = p.make_simplex_map(f)
          for i in p:
            print(i.sign(), i.pair().sign())
            print("%s (%d) - %s (%d)" % (smap[i], i.sign(), smap[i.pair()], i.pair().sign()))
            print("Cycle (%d):" % len(i.cycle), " + ".join((str(smap[ii]) for ii in i.cycle)))
    
          print(" Number of unpaired simplices:", len([i for i in p if i.unpaired()]))
          print(time.asctime())

      else:
          """
          ##############################
          # Dynamic Persistence Chains #
          ##############################
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
          print("Initialize DynamicPersistenceChains...")
          p = DynamicPersistenceChains(f)
                
          print("Pair simplices...")
          p.pair_simplices()
          print(time.asctime())
    
          print("Output persistence...")
          out_path_end1 = '_persistence' + str(kskeleton) + '_diagram_Freq.csv'
          out_path_end2 = '_persistence' + str(kskeleton) + '_data_Freq.csv'
          out_file1 = out_path + table_id + out_path_end1
          out_file2 = out_path + table_id + out_path_end2
          if plot_persistence_diagrams:
            f1 = open(out_file1,"w")
          f2 = open(out_file2,"w")
          smap = p.make_simplex_map(complex)
    
          for i in p:
            if not i.sign():  continue
            birth = smap[i]
            if i.unpaired():
              cycle = i.chain
              death_value = "inf"
            else:
              cycle = i.pair().cycle
              death_value = smap[i.pair()].data
            if birth.data > 0 and birth.data != death_value and \
               birth.data != max_nconcurrences and \
               death_value != max_nconcurrences:
              smap_str = ''
              for ii in cycle: 
                smap_str = smap_str + " " + str(smap[ii])
              ddate = death_value
              bdate = birth.data
              s0 = [str(birth.dimension()),str(bdate),str(ddate)]
              s1 = " ".join(s0)
              s2 = " ".join([s1,smap_str])
              if plot_persistence_diagrams:
                f1.writelines(" ".join([s1,"\n"]))
              f2.writelines(" ".join([s2,"\n"]))
          f2.close()
          if plot_persistence_diagrams:
            f1.close()
            cmd = 'python draw.py ' + out_file1
            print(cmd); os.system(cmd)
          print(time.asctime())
