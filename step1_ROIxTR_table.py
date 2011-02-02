"""
Prepare table of average activity per labeled region.

This program outputs 1 table file per subject,
where each row is a region and columns are time points (e.g., fMRI TRs).

(c) Arno Klein  .  arno@binarybottle.com  .  2010
"""

import os,sys,warnings,glob
warnings.simplefilter('ignore')
from nibabel import load
import numpy as np
from optparse import OptionParser
from pylab import find
import csv

from settings import label_list, label_path, labelfunc_path_end, func_path, func_path_end, table_path, table_end

if __name__ == '__main__':
    table_reader = csv.reader(open(label_list,'r'), delimiter=' ', quotechar='"')
    label_ids = []
    for row0 in table_reader:
        label_ids.append(np.float(row0[0]))
    label_ids = np.unique(label_ids)
    
    # Iterate over subjects
    for subject_path in glob.glob(label_path + "*" + labelfunc_path_end):
        subject_id = subject_path.split(label_path)[-1].split(labelfunc_path_end)[0]
        print(subject_id)

        # Set up the csv file for the subject
        out_file = table_path + subject_id + table_end
        if os.path.exists(out_file):
            pass
        else:
            f = open(out_file,"w")
            label_file = label_path + subject_id + labelfunc_path_end
            func_file = func_path + subject_id + func_path_end
            if os.path.exists(label_file) and os.path.exists(func_file):

                # Iterate over ROIs
                labels = load(label_file).get_data()
                vols = load(func_file).get_data()
                for label_id in label_ids:
                    if label_id > 0:
                        print("Subject " + subject_id + ", label " + str(label_id) + "/" + str(len(label_ids)))
                        label = np.zeros(np.shape(labels))
                        label[labels==label_id] = 1

                        # Iterate over TRs (volumes)
                        f.writelines(str(label_id)+",")
                        for vol_id in range(np.shape(vols)[-1]):
                            vol = vols[:,:,:,vol_id]
                            # get the mean intensity in the ROI for the TR (volume)
                            mean_value = np.mean(np.take(vol,np.nonzero(np.ravel(vol*label))))
                            f.writelines(str(mean_value)+",")
                            print("  Volume " + str(vol_id) + ", mean value " + str(mean_value))
                        f.writelines("\n")
            f.close()
