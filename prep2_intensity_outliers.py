#!/usr/bin/python
"""
Remove intensity outliers identified by RapidArt (called by Nipype in prep1_nipype.py)

(c) Arno Klein  .  arno@binarybottle.com  .  2010
"""

import os
import subprocess
from glob import glob
import nibabel as nib
import numpy as np

volume_by_zero = 1

subject_types = ['patient','control']
for subject_type in subject_types:
    
  # Specify the location of the rapidart artifact statistics
  if subject_type == 'patient'':
    stats_path = './preproc/output/patients/'
  else: 
    stats_path = './preproc/output/controls/'
  stats_path_end = '/art/art.rest_preprocessed.nii_outliers.txt' 

  # Specify the location of the graymatter-masked, motion-corrected data
  local_data_path = stats_path
  local_data_path_end = '/functional/rest_preprocessed_gray.nii.gz'

  # Specify the subject directories
  subject_list = [path.split('/')[-1] for path in glob(os.path.join(local_data_path,'sub*'))]

  for s in subject_list:
    # List of volumes to remove from a given subject    
    vol_list = open(stats_path + s + stats_path_end, 'r').readlines()
    if volume_by_zero:
      vol_list = [int(d)-1 for d in vol_list]
    else:
      vol_list = [int(d) for d in vol_list]
    if len(vol_list) > 0:
      # Load image, remove volumes, and save result
      print('Data path: ' + local_data_path + s + local_data_path_end)
      print('Rapidart output path: ' + stats_path + s + stats_path_end)
      img = nib.load(local_data_path + s + local_data_path_end)
      data = img.get_data()
      keep_vol_list = [k for k in range(data.shape[-1]) if k not in vol_list]
      data2 = np.float64(data[:,:,:,keep_vol_list])
      fpath = ''.join(local_data_path_end.split('/')[0:-1])
      flist = local_data_path_end.split('/')[-1].split('.')
      outfile = local_data_path + s + '/' + fpath + '/' + flist[0] + '_noIntensityOutliers.' + \
              '.'.join(flist[1:len(flist)])
      print('Output file: ' + outfile)
      img2 = nib.Nifti1Image(data2,np.eye(4))
      nib.save(img2,outfile)
    