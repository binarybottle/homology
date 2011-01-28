
import os
import subprocess
from glob import glob
import nibabel as nib
import numpy as np

volume_by_zero = 1

adhd = 1

# Specify the location of the rapidart artifact statistics
if adhd:
  stats_path = '/Users/arno/Documents/Projects/topology_2010/preproc/output/adhd/'
else: 
  stats_path = '/Users/arno/Documents/Projects/topology_2010/preproc/output/controls/'
stats_path_end = '/art/art.rest_preprocessed.nii_outliers.txt' 

# Specify the location of the graymatter-masked, motion-corrected data
data_path = stats_path
data_path_end = '/functional/rest_preprocessed_gray.nii.gz'

# Specify the location of the original data
#if adhd:
#  data_path = '/hd2/data/Brains/FunctionalConnectomes1000/NewYork_a_ADHD/'
#else:
#  data_path = '/hd2/data/Brains/FunctionalConnectomes1000/NewYork_a_part1/'
#data_path_end = '/func/rest.nii.gz'

# Specify the subject directories
subject_list = [path.split('/')[-1] for path in glob(os.path.join(data_path,'sub*'))]

for s in subject_list:
  # List of volumes to remove from a given subject    
  vol_list = open(stats_path + s + stats_path_end, 'r').readlines()
  if volume_by_zero:
    vol_list = [int(d)-1 for d in vol_list]
  else:
    vol_list = [int(d) for d in vol_list]
  if len(vol_list) > 0:
    # Load image, remove volumes, and save result
    print('Data path: ' + data_path + s + data_path_end)
    print('Rapidart output path: ' + stats_path + s + stats_path_end)
    img = nib.load(data_path + s + data_path_end)
    data = img.get_data()
    keep_vol_list = [k for k in range(data.shape[-1]) if k not in vol_list]
    data2 = np.float64(data[:,:,:,keep_vol_list])
    fpath = ''.join(data_path_end.split('/')[0:-1])
    flist = data_path_end.split('/')[-1].split('.')
    outfile = data_path + s + '/' + fpath + '/' + flist[0] + '_noIntensityOutliers.' + \
              '.'.join(flist[1:len(flist)])
    print('Output file: ' + outfile)
    img2 = nib.Nifti1Image(data2,np.eye(4))
    nib.save(img2,outfile)
    