#!/usr/bin/python
"""
Prepare table of average activity per labeled region.

This program outputs 1 table file per subject,
where each row is a region and columns are time points (e.g., fMRI TRs).
The first column contains the label indices.

(c) Arno Klein  .  arno@binarybottle.com  .  2011  .  MIT license
"""

use_slicetimecorrection = 0

data_path = '/hd2/data/Brains/FunctionalConnectomes1000/NewYork_a_ADHD_part1/'
fmri_path = '/func/rest'
file_append = '.nii.gz'
moco_command = 'mcflirt'
slicetime_command = 'slicetimer'
label_list = '/projects/homology/region_nums_names.txt'
table_path = '/projects/homology/output/tables/'
table_end = '_activity.csv'

import os
from nibabel import load
import numpy as np
import csv
import warnings
warnings.simplefilter('ignore')

debug_run1 = 0

if __name__ == '__main__':

    table_reader = csv.reader(open(label_list,'r'), delimiter=' ', quotechar='"')
    label_ids = []
    for row0 in table_reader:
        label_ids.append(np.float(row0[0]))
    label_ids = np.unique(label_ids)

    # Iterate over subjects
    for subject_id in os.listdir(data_path):

        if use_slicetimecorrection:
            func_file = data_path + subject_id + fmri_path + '_' + moco_command + '_' + slicetime_command + file_append
        else:
            func_file = data_path + subject_id + fmri_path + '_' + moco_command + file_append
        label_file = data_path + subject_id + fmri_path + '_aparc2aseg' + file_append
        out_table_file = table_path + subject_id + table_end

        # Set up the csv file for the subject
        try:
            f = open(out_table_file,"w")
        except IOError:
            raise

        """
        Fill each table row with the average activity values for a given labeled region across time (columns).
        """
        # Iterate over labels
        try:
            labels = load(label_file).get_data()
            vols = load(func_file).get_data()
        except IOError:
            raise

        for label_id in label_ids:
            if label_id > 0:
                print("Subject " + subject_id + ", label " + str(label_id) + "/" + str(len(label_ids)))
                label = np.zeros(np.shape(labels))
                label[labels==label_id] = 1
                # Iterate over columns (volumes at different time points)
                f.writelines(str(label_id)+",")
                for vol_id in range(np.shape(vols)[-1]):
                    vol = vols[:,:,:,vol_id]
                    # get the mean intensity in the ROI for the TR (volume)
                    Inonzero = np.nonzero(np.ravel(vol*label))
                    if np.size(Inonzero) > 0:
                        mean_value = np.mean(np.take(vol,Inonzero))
                    else:
                        mean_value = 0
                    f.writelines(str(mean_value)+",")
                    #print("  Volume " + str(vol_id) + ", mean value " + str(mean_value))
                f.writelines("\n")
        f.close()

        if debug_run1:
            raise NameError('STOPPED')