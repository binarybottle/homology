#!/usr/bin/python
import os,sys,warnings,glob
warnings.simplefilter('ignore')
from nibabel import load
import numpy as np
from optparse import OptionParser
from pylab import find
import csv

base_path = "/projects/topology_2010/"
data_path = "/hd2/data/Brains/FunctionalConnectomes1000/"
label_path = data_path + "NewYork_freesurfer_labels/"
label_path_end = '_labels_funcspace.nii.gz'
func_path = '/projects/topology_2010/preproc/workingdir/level1/preproc/_subject_id_'
func_path_end = '/realign/rest_dtype_mcf.nii.gz'
out_path = '/projects/topology_2010/output/tables/ROIxTR/'
label_list = '/projects/topology_2010/region_nums_names.txt'

"""
This program outputs 1 csv file per subject,
where each row is a region and columns are fMRI TRs.
"""
if __name__ == '__main__':
    table_reader = csv.reader(open(label_list,'r'), delimiter=' ', quotechar='"')
    label_ids = []
    for row0 in table_reader:
        label_ids.append(np.float(row0[0]))
    label_ids = np.unique(label_ids)
    
    # Iterate over subjects
    for subject_path in glob.glob(label_path + "*" + label_path_end):
        subject_id = subject_path.split(label_path)[-1].split(label_path_end)[0]
        print(subject_id)

        # Set up the csv file for the subject
        out_file = out_path + subject_id + "_ROIvsTR.csv"
        if os.path.exists(out_file):
            pass
        else:
            f = open(out_file,"w")
            label_file = label_path + subject_id + label_path_end
            func_file = func_path + subject_id + func_path_end
            if os.path.exists(label_file) and os.path.exists(func_file):

                # Iterate over ROIs
                labels = load(label_file).get_data()
                vols = load(func_file).get_data()
                ##label_ids = np.unique(labels.ravel())
                ##data = np.zeros((len(label_ids),len(vols)))
                for label_id in label_ids:
                    if label_id > 0:
                        print("Subject " + subject_id + ", label " + str(label_id) + "/" + str(len(label_ids)))
                        label = np.zeros(np.shape(labels))
                        label[labels==label_id] = 1
                        #label_voxels = np.nonzero(label)

                        # Iterate over TRs (volumes)
                        f.writelines(str(label_id)+",")
                        for vol_id in range(np.shape(vols)[-1]):
                            vol = vols[:,:,:,vol_id]
                            # get the mean intensity in the ROI for the TR (volume)
                            mean_value = np.mean(np.take(vol,np.nonzero(np.ravel(vol*label))))
                            #data[label_id,vol_id] = mean_value
                            f.writelines(str(mean_value)+",")
                            print("  Volume " + str(vol_id) + ", mean value " + str(mean_value))
                        f.writelines("\n")
            f.close()
            #np.save(out_path + subject_id + "_data.npy",data)
