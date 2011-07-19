#!/usr/bin/python
"""
Compute persistence from a binary table of activity data.

Persistence code was developed by Dmitriy Morozov (Dionysus) and Vidit Nanda (nmfsimtop).

(c) Arno Klein  .  arno@binarybottle.com  .  2011  .  MIT license
"""

kskeleton = 3  # A k-simplex has k+1 vertices
reverse_filtration_order = 1
persistence_type = 3  # static_persistence = 1; dynamic_persistence = 2; nmfsimtop = 3
remove_dimension1 = 1

data_path = '/Users/arno/Data/Brains/FunctionalConnectomes1000/NewYork_a_ADHD_part1/'
table_path = '/projects/homology/output/tables/'
table_end = '_binary.csv'
nconcurrences_file_end = '_concurrences.txt'
first_column = 1 # 0-based

import sys, os
from subprocess import call
import csv
import numpy as np
import pylab as plt
from itertools import combinations
import time

debug_run1 = 1
test = 1
if test:
    remove_dimension1 = 0

if persistence_type == 1 or persistence_type == 2:
    from dionysus import Simplex, data_dim_cmp, dim_data_cmp, closure, Filtration, StaticPersistence, DynamicPersistenceChains

    plot_persistence_diagrams = 0

if __name__ == '__main__':

# Iterate over subjects
    for subject_id in os.listdir(data_path):
        table_file = table_path + subject_id + table_end
        print('Load binary activity table: ' + table_file)
        if test:
            table_files = ['test_complex']

            table_indices = [[64], [26, 35], [54], [69], [2], [64], [16, 35, 82], [26, 35], [54], [69],
                [2], [64], [16, 35, 82], [26, 35], [54], [69], [33, 81], [2], [64],
                [16, 35, 82], [26, 35], [54], [69], [8, 71], [33, 81], [2]]
            test_nconcurrences = np.array([4, 4, 4, 4, 4, 4, 3, 4, 4, 4,
                                           4, 4, 3, 4, 4, 4, 2, 4, 4,
                                           3, 4, 4, 4, 1, 2, 4])

            table_indices = [ [1,2], [1,3], [3,4], [1,2], [1,3], [3,4], [2,4], [1,2], [2,3], [1,3], [2,4], [3,4],
                            [2,3,4], [1,2], [1,3], [2,3,4], [1,2,3], [5,6] ]
 
            table_indices = [ [1,2], [2,3], [4], [5,6], [1,6],
                [1,2], [2,3], [3,5], [4], [5,6], [1,6],
                [1,2], [2,3], [3,5], [5,6], [1,6], [3,4], [4,5], [1,7], [2,7],
                [1,2], [2,3], [5,6], [1,6], [3,4,5], [1,7], [2,7], [6,7],
                [1,2], [2,3], [5,6], [1,6], [3,4,5], [1,7], [2,7], [6,7], [3,7],
                [1,2], [2,3], [5,6], [1,6], [3,4,5], [1,7], [2,7], [6,7], [3,7], [5,7],
                [1,2,7], [2,3], [5,6], [1,6], [3,4,5], [6,7], [3,7], [5,7] ]

            table_indices = [[ 2, 3, 5, 13, 14, 21, 26, 27, 28, 30, 35, 38, 39, 41, 46, 47, 51, 52, 55, 58, 61, 62, 64,  65 ],
                [ 2, 3, 5, 13, 14, 17, 21, 24, 27, 30, 38, 39, 41, 46, 47, 49, 51, 52, 55, 61, 64, 65,  67 ],
                [ 2, 3, 5, 7, 13, 14, 17, 19, 21, 23, 24, 27, 28, 30, 31, 36, 38, 39, 40, 41, 46, 47, 49, 51, 52, 54, 55, 59, 61, 64, 65, 67, 69, 72, 73,  74 ],
                [ 2, 3, 7, 10, 12, 13, 14, 17, 19, 22, 23, 24, 27, 28, 30, 31, 38, 40, 41, 47, 49, 52, 54, 56, 59, 61, 62, 67, 72, 73,  74 ],
                [ 2, 3, 10, 12, 13, 14, 24, 28, 33, 41, 47, 56, 59,  74 ],
                [ 2, 10, 24,  33 ],
                [ 2, 12, 24,  33 ],
                [ 2, 5, 12, 24, 33, 48, 51,  59 ],
                [ 2, 5, 12, 24, 33, 35, 42, 47, 48, 51, 59, 63, 64, 69,  72 ],
                [ 2, 5, 7, 10, 12, 18, 22, 23, 24, 27, 28, 29, 35, 39, 41, 42, 44, 47, 48, 49, 51, 54, 58, 60, 61, 62, 63, 64, 65, 66, 69, 71, 72,  74 ],
                [ 2, 5, 10, 12, 23, 24, 28, 41, 44, 47, 51, 58, 61, 63, 64, 66, 68, 71, 73,  74 ],
                [ 5, 10, 12, 24, 41, 61, 66, 68,  71 ],
                [ 24 ],
                [ 51,  59 ],
                [ 2, 26, 47, 51,  69 ],
                [ 2, 18, 23, 26, 28, 47, 54, 58, 64,  66 ],
                [ 2, 23, 26, 28, 47, 66,  71 ],
                [ 26, 28,  47 ],
                [ 70 ],
                [ 7, 26, 51, 53, 54,  70 ],
                [ 5, 7, 26, 44, 51, 53, 54, 58, 69, 70,  71 ],
                [ 5, 7, 26, 44, 51, 54, 66,  71 ],
                [ 2, 44,  66 ],
                [ 2, 39, 52,  59 ],
                [ 2, 4, 5, 9, 13, 17, 19, 24, 25, 34, 36, 39, 42, 51, 52,  63 ],
                [ 4, 5, 9, 13, 17, 19, 20, 24, 25, 34, 36, 39, 40, 42, 46, 48, 51, 52, 53, 55, 57, 61, 63, 65,  69 ],
                [ 3, 4, 5, 9, 13, 14, 17, 19, 20, 24, 25, 34, 35, 36, 39, 40, 46, 52, 53, 55, 57, 61, 63, 65, 68, 69,  73 ],
                [ 4, 5, 9, 13, 17, 20, 34, 35, 39, 52, 61, 63, 68,  73 ],
                [ 73 ],
                [ 59 ],
                [ 59 ],
                [ 17, 26,  59 ],
                [ 9, 17, 20, 25, 26, 50, 59,  73 ],
                [ 9, 17, 20, 50,  73 ],
                [ 27 ],
                [ 27,  32 ],
                [ 32 ],
                [ 32 ],
                [ 26 ],
                [ 9,  26 ],
                [ 16, 26, 44, 50,  61 ],
                [ 16, 43,  50 ],
                [ 16, 43,  66 ],
                [ 16, 51,  66 ],
                [ 16, 36, 46, 51,  66 ],
                [ 16, 31, 36, 44,  71 ],
                [ 16, 31, 35, 36, 38, 43, 44, 68, 69,  71 ],
                [ 32, 35, 38, 44,  68 ],
                [ 8, 38,  59 ],
                [ 8, 38,  59 ],
                [ 8, 15, 44,  59 ],
                [ 44, 45,  54 ],
                [ 6, 44,  54 ],
                [ 26 ],
                [ 26 ],
                [ 44,  46 ],
                [ 16, 29, 44, 45, 46, 54, 56,  59 ],
                [ 16, 29, 36, 37, 43, 45, 46, 51, 54, 59,  67 ],
                [ 7, 9, 10, 16, 21, 24, 29, 34, 36, 42, 43, 45, 46, 49, 55, 59, 66,  67 ],
                [ 4, 7, 9, 10, 13, 14, 16, 19, 20, 21, 22, 25, 29, 31, 34, 36, 39, 40, 42, 43, 45, 46, 47, 49, 52, 53, 55, 57, 58, 59, 60, 61, 63, 64, 65, 66, 67, 69, 71,  74 ],
                [ 4, 8, 9, 12, 13, 14, 16, 17, 19, 20, 21, 22, 25, 27, 28, 29, 31, 33, 34, 35, 36, 38, 39, 40, 42, 45, 46, 47, 48, 49, 52, 53, 55, 57, 58, 60, 61, 62, 63, 64, 65, 66, 68, 69, 71, 73,  74 ],
                [ 4, 9, 13, 14, 17, 20, 25, 28, 33, 34, 39, 40, 41, 47, 48, 52, 53, 57, 58, 61, 62, 68, 73,  74 ],
                [ 4, 9, 13, 20, 25, 34, 40, 44,  52 ],
                [ 4 ],
                [ 4 ],
                [ 4, 19, 25,  59 ],
                [ 4, 17, 19, 25, 59,  66 ],
                [ 17, 25, 26, 27,  66 ],
                [ 26 ],
                [ 43 ],
                [ 62 ],
                [ 27, 44, 58, 62, 66,  72 ],
                [ 7, 27, 29, 44, 53, 58, 60, 65, 66, 72,  74 ],
                [ 29, 42, 44, 46, 65,  66 ],
                [ 29, 65,  66 ],
                [ 8, 21, 22, 31, 38, 45, 55,  65 ],
                [ 4, 6, 7, 8, 11, 15, 16, 18, 19, 20, 21, 23, 31, 32, 35, 38, 40, 45, 48, 50, 53, 54, 55, 56, 58, 60, 67, 69, 71, 72,  74 ],
                [ 1, 6, 8, 11, 15, 18, 20, 23, 27, 28, 31, 32, 33, 35, 37, 38, 39, 40, 45, 47, 48, 50, 53, 54, 56, 58, 62, 66, 70, 71, 72,  74 ],
                [ 1, 6, 8, 11, 18, 23, 27, 32, 45, 50, 56, 58, 66,  70 ],
                [ 6, 8, 11, 18, 32,  70 ],
                [ 1, 6, 8, 11, 18, 32,  70 ],
                [ 1, 3, 6, 8, 11, 15, 16, 18, 30, 32, 38, 60,  62 ],
                [ 1, 3, 6, 7, 8, 11, 15, 16, 18, 21, 30, 32, 37, 38, 45, 53, 57, 60, 62, 70,  72 ],
                [ 1, 3, 6, 7, 8, 11, 15, 18, 22, 32, 41, 42, 43, 45, 53, 57, 60, 62, 70,  72 ],
                [ 1, 6, 7, 11, 15, 42, 43, 45, 60, 70,  71 ],
                [ 1, 11, 43, 53, 55,  71 ],
                [ 21, 31, 43, 46, 49, 53, 55, 60, 67,  71 ],
                [ 1, 3, 6, 7, 10, 11, 16, 21, 22, 31, 36, 46, 49, 53, 55, 60, 67, 69,  71 ],
                [ 1, 3, 6, 7, 11, 15, 16, 18, 21, 22, 29, 31, 32, 49, 60, 67, 69, 70, 71,  72 ],
                [ 3, 6, 7, 11, 14, 15, 21, 22, 29, 32, 43, 60, 67, 70,  71 ],
                [ 3, 4, 6, 7, 11, 14, 15, 21, 29, 65,  70 ],
                [ 1, 3, 4, 6, 7, 9, 11, 14, 15, 18, 20, 21, 29, 34, 38, 45, 46, 49, 53, 56, 62, 64, 65, 67, 69,  70 ],
                [ 1, 3, 4, 6, 7, 8, 9, 11, 14, 15, 17, 18, 19, 20, 21, 22, 23, 25, 29, 30, 31, 33, 34, 35, 36, 37, 38, 39, 40, 42, 45, 46, 47, 48, 49, 50, 52, 53, 55, 56, 57, 60, 62, 63, 64, 65, 67, 68, 69, 70, 71, 72,  74 ],
                [ 1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 45, 46, 47, 48, 49, 50, 52, 53, 54, 55, 56, 57, 58, 60, 61, 62, 63, 64, 65, 67, 68, 69, 70, 71, 72, 73,  74 ],
                [ 3, 4, 6, 7, 8, 9, 10, 11, 12, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 39, 40, 41, 42, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 60, 61, 62, 63, 64, 65, 67, 68, 69, 70, 71, 72, 73,  74 ],
                [ 1, 3, 4, 7, 8, 9, 10, 11, 12, 14, 15, 16, 18, 21, 22, 23, 24, 25, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 39, 41, 42, 45, 46, 47, 48, 49, 52, 53, 54, 55, 56, 57, 58, 60, 61, 62, 63, 65, 67, 68, 69, 70, 72, 73,  74 ],
                [ 1, 3, 7, 10, 11, 12, 14, 15, 16, 18, 21, 22, 23, 24, 25, 28, 30, 32, 33, 34, 35, 36, 37, 39, 41, 42, 44, 45, 46, 47, 48, 49, 52, 53, 54, 55, 56, 57, 58, 59, 60, 62, 63, 65, 67, 68, 70, 72, 73,  74 ],
                [ 1, 3, 10, 11, 14, 15, 16, 18, 21, 22, 23, 28, 30, 32, 35, 36, 37, 41, 42, 43, 44, 45, 46, 47, 55, 56, 57, 58, 59, 60, 63, 64, 65, 67, 68, 70,  72 ],
                [ 1, 3, 6, 11, 15, 18, 21, 22, 23, 30, 32, 35, 37, 42, 43, 46, 50, 52, 55, 57, 60, 64, 65, 68, 70,  72 ],
                [ 3, 6, 11, 14, 15, 18, 20, 22, 23, 27, 32, 33, 35, 37, 42, 43, 48, 49, 50, 52, 55, 57, 60, 61, 64, 68, 69, 70, 71, 72,  74 ],
                [ 6, 11, 12, 14, 15, 17, 18, 20, 22, 23, 27, 29, 30, 32, 33, 35, 37, 40, 42, 47, 48, 49, 50, 51, 52, 53, 55, 56, 57, 58, 60, 61, 62, 63, 65, 67, 68, 69, 71, 72, 73,  74 ],
                [ 1, 4, 6, 7, 8, 11, 12, 14, 15, 18, 19, 20, 22, 23, 25, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 45, 47, 48, 49, 50, 52, 53, 54, 55, 56, 57, 58, 60, 61, 62, 63, 65, 67, 68, 69, 70, 71, 72, 73,  74 ],
                [ 1, 7, 8, 12, 14, 16, 18, 19, 22, 23, 25, 27, 28, 30, 31, 33, 34, 35, 36, 37, 38, 40, 45, 47, 48, 49, 50, 53, 54, 55, 56, 57, 58, 62, 63, 65, 67, 68, 70, 72,  73 ],
                [ 1, 10, 14, 18, 22, 23, 31, 36, 37, 38, 42, 45, 46, 47, 48, 49, 50, 53, 55, 56, 58, 65, 67, 68, 70, 72,  73 ],
                [ 1, 10, 18, 22, 23, 31, 36, 42, 43, 45, 46, 49, 50, 53, 55, 56, 64, 65, 67, 70, 73,  74 ],
                [ 5, 6, 8, 11, 12, 15, 18, 19, 21, 22, 23, 25, 27, 29, 31, 32, 33, 35, 36, 37, 39, 42, 43, 45, 48, 49, 50, 52, 53, 55, 56, 60, 62, 63, 64, 65, 67, 69, 70, 72,  74 ],
                [ 1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 17, 18, 20, 21, 22, 23, 25, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 45, 47, 48, 49, 50, 52, 53, 54, 55, 56, 57, 58, 60, 62, 63, 64, 67, 69, 70, 72,  74 ],
                [ 1, 3, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 17, 18, 20, 22, 23, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 45, 47, 48, 49, 50, 52, 53, 54, 55, 56, 58, 60, 62, 64, 66, 67, 69, 70, 72,  74 ],
                [ 1, 3, 6, 7, 8, 10, 11, 12, 15, 16, 20, 23, 26, 27, 28, 29, 30, 32, 33, 37, 38, 41, 45, 47, 50, 56, 58, 62, 66, 69,  72 ],
                [ 1, 3, 6, 8, 10, 11, 15, 16, 23, 27, 29, 32, 33, 37, 38, 43, 56, 62,  72 ],
                [ 1, 3, 6, 8, 10, 11, 15, 16, 29, 32, 33, 43,  54 ],
                [ 1, 6, 7, 8, 11, 15, 16, 18, 19, 21, 29, 30, 31, 32, 33, 35, 36, 37, 38, 39, 40, 41, 43, 45, 46, 48, 50, 52, 54, 57, 63, 66, 67, 70, 72,  74 ],
                [ 1, 3, 4, 6, 7, 8, 9, 11, 12, 15, 16, 18, 19, 20, 21, 22, 25, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 43, 44, 45, 46, 48, 49, 50, 52, 54, 56, 57, 58, 62, 63, 64, 67, 68, 69, 70, 71, 72, 73,  74 ],
                [ 1, 3, 4, 6, 7, 8, 9, 11, 12, 15, 16, 17, 18, 19, 20, 21, 22, 25, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 43, 44, 45, 46, 47, 48, 49, 50, 52, 54, 55, 56, 57, 58, 60, 62, 63, 64, 67, 68, 69, 71, 72, 73,  74 ],
                [ 1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 27, 29, 30, 31, 33, 34, 35, 36, 37, 38, 39, 40, 41, 43, 45, 46, 48, 49, 50, 52, 54, 55, 56, 57, 58, 60, 61, 62, 63, 64, 67, 68, 69, 71, 72, 73,  74 ],
                [ 1, 3, 4, 6, 8, 9, 10, 11, 12, 15, 16, 17, 19, 20, 21, 22, 23, 24, 25, 27, 29, 30, 31, 33, 34, 35, 37, 38, 39, 40, 41, 43, 46, 48, 50, 53, 54, 55, 56, 57, 58, 60, 61, 62, 63, 64, 67, 68, 69, 70, 73,  74 ],
                [ 1, 3, 4, 6, 7, 8, 10, 11, 12, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 29, 30, 31, 33, 34, 35, 37, 38, 39, 40, 41, 42, 43, 46, 47, 48, 49, 50, 53, 54, 55, 56, 57, 58, 60, 62, 63, 64, 67, 68, 69, 70, 73,  74 ],
                [ 1, 3, 4, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 45, 47, 48, 49, 50, 53, 54, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 72, 73,  74 ],
                [ 1, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 47, 48, 49, 50, 52, 53, 54, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73,  74 ],
                [ 1, 3, 5, 7, 10, 12, 13, 15, 18, 19, 20, 22, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 35, 37, 38, 39, 40, 41, 42, 43, 44, 45, 47, 48, 49, 50, 53, 54, 56, 57, 58, 60, 61, 62, 63, 64, 68, 70, 71, 72, 73,  74 ],
                [ 1, 3, 5, 10, 12, 13, 19, 20, 24, 26, 27, 28, 29, 30, 33, 37, 40, 41, 42, 43, 48, 49, 50, 56, 57, 60, 61, 62, 63, 64, 68, 70, 71,  73 ],
                [ 1, 5, 8, 10, 12, 13, 19, 20, 22, 24, 27, 28, 30, 31, 37, 40, 41, 42, 43, 46, 48, 50, 53, 56, 57, 60, 61, 63, 64,  70 ],
                [ 1, 5, 6, 7, 8, 9, 12, 13, 15, 17, 18, 19, 20, 21, 22, 23, 28, 30, 31, 33, 35, 36, 37, 40, 41, 42, 43, 46, 48, 49, 50, 53, 54, 55, 56, 57, 58, 60, 63, 64, 67, 70,  74 ],
                [ 1, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 28, 30, 31, 33, 35, 36, 37, 39, 40, 41, 42, 43, 44, 46, 47, 48, 49, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 63, 64, 66, 67, 68, 72, 73,  74 ],
                [ 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 25, 28, 30, 31, 33, 36, 37, 39, 40, 41, 42, 43, 44, 46, 47, 48, 50, 56, 57, 58, 59, 60, 63, 66, 68, 72, 73,  74 ],
                [ 4, 5, 8, 9, 12, 13, 16, 17, 19, 25, 30, 36, 37, 40, 41, 42, 43, 44, 50, 57, 58, 60, 68,  73 ],
                [ 4, 5, 8, 9, 12, 13, 21, 30, 43, 44, 57, 66, 68,  73 ],
                [ 2, 5, 9, 13, 20, 21, 23, 28, 30, 35, 42, 64, 65, 66, 68,  73 ],
                [ 2, 13, 21, 23, 28, 31, 35, 41, 42, 62, 65, 66, 68,  73 ],
                [ 2, 10, 13, 26, 28, 41, 42, 65,  66 ],
                [ 2, 26, 27,  41 ],
                [ 27 ],
                [ 71 ],
                [ 71 ],
                [ 26 ],
                [ 26 ],
                [ 2 ],
                [ 2 ],
                [ 9, 13, 48, 57,  63 ],
                [ 9, 10, 12, 13, 17, 19, 20, 22, 29, 30, 33, 34, 35, 38, 40, 42, 48, 57, 59, 63, 64, 73,  74 ],
                [ 4, 9, 10, 12, 13, 16, 17, 19, 20, 21, 22, 25, 29, 30, 33, 34, 36, 37, 38, 40, 41, 42, 43, 44, 45, 48, 50, 54, 55, 57, 59, 61, 63, 64, 68, 73,  74 ],
                [ 2, 4, 5, 8, 9, 10, 12, 13, 16, 17, 19, 20, 24, 25, 28, 29, 30, 33, 34, 36, 37, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 52, 54, 55, 56, 57, 59, 61, 62, 63, 64, 67, 68, 73,  74 ],
                [ 2, 4, 5, 8, 9, 10, 12, 13, 19, 20, 24, 25, 28, 29, 34, 37, 40, 41, 43, 45, 46, 47, 49, 50, 51, 53, 54, 56, 59, 61, 63, 64, 65, 67, 68, 73,  74 ],
                [ 2, 3, 5, 10, 24, 25, 26, 43, 45, 47, 51, 56, 61, 64, 65, 68,  73 ],
                [ 2, 3, 14, 26,  27 ],
                [ 2, 14, 26,  27 ],
                [ 2, 26, 27,  44 ],
                [ 44,  66 ],
                [ 66 ],
                [ 51,  71 ],
                [ 51,  71 ],
                [ 51,  59 ],
                [ 44, 51,  59 ],
                [ 2, 26, 51, 59,  65 ],
                [ 2, 21, 26, 46, 51, 59,  65 ],
                [ 26 ],
                [ 27 ],
                [ 59 ],
                [ 2, 5, 24, 34, 59,  69 ],
                [ 2, 5, 24, 26, 34, 61,  69 ],
                [ 2, 5, 13, 24, 26, 34, 51, 52, 61,  69 ],
                [ 5, 13, 23, 24, 26, 34, 40, 44, 51, 52, 61,  69 ],
                [ 4, 5, 9, 13, 17, 19, 24, 25, 34, 39, 40, 44, 51, 52, 55, 61, 69,  71 ],
                [ 4, 5, 9, 10, 13, 17, 19, 24, 25, 34, 39, 44, 51, 52, 55, 59, 61, 66,  71 ],
                [ 4, 5, 9, 13, 17, 19, 24, 25, 34, 39, 52, 61, 66, 69,  71 ],
                [ 4, 5, 9, 17, 19, 25, 34, 39, 52, 61, 66,  71 ],
                [ 4, 5, 9, 17, 34, 39, 52,  61 ],
                [ 14 ],
                [ 14, 23, 24, 27,  32 ],
                [ 2, 14, 23, 26, 27,  32 ],
                [ 2, 14, 23, 26, 32, 38,  69 ],
                [ 14, 32,  38 ],
                [ 14, 16,  65 ],
                [ 10, 14, 16, 28, 49, 54, 62, 65, 67,  72 ],
                [ 2, 10, 14, 16, 28, 44, 46, 49, 53, 54, 62, 64,  72 ],
                [ 2, 10, 14, 38, 51,  54 ],
                [ 38,  51 ],
                [ 51 ],
                [ 51 ],
                [ 51 ],
                [ 17, 44, 51,  66 ],
                [ 36, 44, 51,  66 ],
                [ 36,  71 ],
                [ 31,  59 ],
                [ 28, 31, 58,  59 ],
                [ 26, 28, 35, 37, 39, 51, 58, 62,  65 ]]

            nconcurrences = np.zeros(len(table_indices), dtype=int)
            iconcurrences = 0
            for isimplex, simplex in enumerate(table_indices):
                for simplex2 in table_indices:
                    if len(np.intersect1d(simplex,simplex2)) == len(simplex):
                        nconcurrences[isimplex] += 1

            print('table_indices:')
            print(table_indices)

        else:
            """
            Load frequency filtration numbers.
            """
            num_file = table_path + subject_id + nconcurrences_file_end
            print('Load filtration file: ' + num_file)
            nconcurrences_all = np.loadtxt(num_file)

            """
            Import table and extract all non-empty rows (not incl. first column).
            """
            table_reader = csv.reader(open(table_file, 'r'), delimiter = ',', quotechar = '"')
            [nrows, ncols] = np.shape([s for s in table_reader])
            ncols = ncols - first_column
            print('Number of columns = ' + str(ncols))
            print('Number of rows = ' + str(nrows))
            table = np.zeros((nrows, ncols))
            table_reader = csv.reader(open(table_file, 'r'), delimiter = ',', quotechar = '"')
            for irow, row in enumerate(table_reader):
                table[irow] = [np.int(np.float(s)) for s in row if s != ''][first_column::]

            """
            Transpose table and create a new list of lists of indices for each original table column.
            """
            table_indices = []
            nconcurrences = []
            for icol, col in enumerate(np.transpose(table)):
                Icol = np.nonzero(col)
                if len(Icol[0]) > 0:
                    table_indices.append([s for s in Icol[0]])
                    nconcurrences.append(nconcurrences_all[icol])

        """
        Convert number of concurrences to filtration order (max is time 0).
        """
        max_nconcurrences = max(nconcurrences)
        print('Maximum number of concurrences = ' + str(max_nconcurrences))
        print('Filtrations = ' + str(nconcurrences))
        if reverse_filtration_order:
            print('Reverse filtrations = ' + str(max_nconcurrences - nconcurrences + 1))
            nconcurrences = max_nconcurrences - nconcurrences + 1
        print(time.asctime())

        """
        ###############
        # Persistence #
        ###############
        """
        if persistence_type == 1 or persistence_type == 2:
            print('--- Dionysus software for persistence homology ---')

            # Create simplices
            print('Construct and sort simplices...')
            levels = []
            for itime, data_time in enumerate(table_indices):
                if remove_dimension1:
                    if reverse_filtration_order:
                        if nconcurrences[itime] < max_nconcurrences:
                            levels.append(Simplex([int(s) for s in data_time], nconcurrences[itime]))
                    else:
                        if nconcurrences[itime] > 1:
                            levels.append(Simplex([int(s) for s in data_time], nconcurrences[itime]))
                else:
                    levels.append(Simplex([int(s) for s in data_time], nconcurrences[itime]))

            # Sort the list by data
            levels.sort(key = lambda s: s.data)
            print(time.asctime())

            # Include all faces in each simplex
            # Compute the k-skeleton of the closure of the list of simplices.
            # A k-simplex has k+1 vertices.
            print("Compute all " + str(kskeleton) + "-skeleton faces for each simplex...")
            complex = closure(levels, kskeleton + 1)
            print(str(complex.__len__()) + ' faces computed')
            print(time.asctime())

            print("Apply Filtration")
            f = Filtration(complex, dim_data_cmp)
            #print("Complex in the filtration order:" + ', '.join((str(s) for s in f)))
            print(time.asctime())

        if persistence_type == 1:
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
                print("dim %d: %s (%d) - %s (%d)" % (
                    smap[i].dimension(), smap[i], i.sign(), smap[i.pair()], i.pair().sign()))
                #print(i.sign(), i.pair().sign())
                #print("%s (%d) - %s (%d)" % (smap[i], i.sign(), smap[i.pair()], i.pair().sign()))
                #print("Cycle (%d):" % len(i.cycle), " + ".join((str(smap[ii]) for ii in i.cycle)))
            print("Number of unpaired simplices: %d" % (len([i for i in p if i.unpaired()])))
            print(time.asctime())

        elif persistence_type == 2:
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
            out_file1 = table_path + subject_id + out_path_end1
            out_file2 = table_path + subject_id + out_path_end2
            if not test:
                if plot_persistence_diagrams:
                    f1 = open(out_file1, "w")
                f2 = open(out_file2, "w")

            smap = p.make_simplex_map(f)
            for i in p:
                #print("dim %d: %s (%d) - %s (%d)" % (smap[i].dimension(), smap[i], i.sign(), smap[i.pair()], i.pair().sign()))
                if not i.sign():  continue
                birth = smap[i]
                if i.unpaired():
                    cycle = i.chain
                    death_value = "inf"
                else:
                    cycle = i.pair().cycle
                    death_value = smap[i.pair()].data
                    #print(birth.data, death_value, max_nconcurrences)
                if birth.data > 0 and birth.data != death_value and\
                   birth.data != max_nconcurrences and\
                   death_value != max_nconcurrences:
                    smap_str = ''
                    for ii in cycle:
                        smap_str = smap_str + " " + str(smap[ii])
                    ddate = death_value
                    bdate = birth.data
                    s0 = [str(birth.dimension()), str(bdate), str(ddate)]
                    s1 = " ".join(s0)
                    s2 = " ".join([s1, smap_str])
                    print(" ".join([s2, "\n"]))
                    if not test:
                        if plot_persistence_diagrams:
                            f1.writelines(" ".join([s1, "\n"]))
                        f2.writelines(" ".join([s2, "\n"]))
            if not test:
                f2.close()
                if plot_persistence_diagrams:
                    f1.close()
                    cmd = 'python draw.py ' + out_file1
                    print(cmd);
                    os.system(cmd)
            print(time.asctime())

        elif persistence_type == 3:
            """
            This program calls code developed by Vidit Nanda:
            pers <input file name> nmfsimtop <output file string>

            "Non-ManiFold SIMplicial TOPlex" is
            the kind of cell complex that you are creating here.
            <input filename> should point to a simple text file which contains
            numbers in the following format (without angle brackets or any
            punctuation whatsoever save spaces and newlines):
            -----------------------------------------------
			<dimension of point-space, say n> <dimension cap, d>
			<dim of simplex 1, say m> <coordinates of 1st vertex> ... <coordinates of m+1 vertex>
			<dim of simplex 2,...> etc.
			:
			------------------------------------------------
			Coordinates are separated by spaces.
            Here n is the dimension of the ambient space whose points form the
            vertices of your simplices. Each line following the <n> represents a
            single simplex. The first number (d1) indicates its dimension. 
            We now know that there are (d1 + 1) vertices for this simplex, each being
            a point with n coordinates. So the next n(d1 + 1) numbers are
            coordinates for the vertices of the simplex. The last number b1 is the
            birth time of that simplex."
            
            EXAMPLE:
            For our binary table input:

                T1   T2   T3    T4
            S1  X    X          X
            S2  X    X
            S3       X    X

            Filtration works as follows:

            T1: <1,2> appears twice
            T2: <1,2,3> appears once
            T3: <3> appears twice
            T4: <1> appears three times

            The dimensions and indices and birth numbers (our frequency levels) are:

            1 1 2 2
            2 1 2 3 1
            0 3 2
            0 1 3

            Removing filtration level 1 (simplices that appear only one time):

            1 1 2 2
            0 3 2
            0 1 3

            Filtration is in reverse order as conventional persistence, 
            so input to Vidit Nanda's program is therefore:

            1 3
            1 1 2 1
            0 3 1
            0 1 0
            """
            nmfsimtop_input_file = table_path + 'nmfsimtop/' + subject_id + '_nmfsimtop_input.txt'
            nmfsimtop_output_string = table_path + 'nmfsimtop/' + subject_id + '_nmfsimtop'
            f3 = open(nmfsimtop_input_file, "w")
            f3.close()
            f3 = open(nmfsimtop_input_file, "a")
            f3.write("1 " + str(kskeleton) + "\n")
            print('Creating NMFSimTop input file: ' + nmfsimtop_input_file)
            for itime, data_time in enumerate(table_indices):
                if len(data_time) > 0:
                    write_string = " ".join([str(len(data_time) - 1), " ".join([str(s) for s in data_time]),
                                             str(np.int(nconcurrences[itime])), "\n"])
                    f3.close()
                    f3 = open(nmfsimtop_input_file, "a")
                    if remove_dimension1:
                        if reverse_filtration_order and nconcurrences[itime] < max_nconcurrences:
                            f3.write(write_string)
                        elif nconcurrences[itime] > 1:
                            f3.write(write_string)
                    else:
                        f3.write(write_string)

            f3.close()
            args = " ".join(
                ['/Users/arno/Software/Pers3/pers', 'nmfsimtop', nmfsimtop_input_file, nmfsimtop_output_string])
            print(args);
            print('Running NMFSimTop...')
            p = call(args, shell = "True")

        if debug_run1:
            raise(Exception('Done with debug run.'))
