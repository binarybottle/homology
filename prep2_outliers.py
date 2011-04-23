#!/usr/bin/python
"""
1. Find motion and intensity outliers.using RapidArt (called by NiPype)
2. Remove intensity outlier volumes or replace them "-1" values.

(c) Arno Klein  .  arno@binarybottle.com  .  2011  .  MIT license
"""

detect_outliers = 1
correct_outliers = 0

import os
import nibabel as nb
import numpy as np
import nipype.algorithms.rapidart as rapidart
from settings import data_path, fmri_path, file_append, moco_command, stats_path, stats_path_end, remove_volumes

for subject_id in os.listdir(data_path):

    """
    Find motion and intensity outliers.
    """
    if detect_outliers:

        moco_file = data_path + subject_id + fmri_path + '_' + moco_command + file_append
        brain_fmri_file = data_path + subject_id + fmri_path + '_brain' + file_append

        ad = rapidart.ArtifactDetect()
        ad.inputs.realigned_files = moco_file
        ad.inputs.mask_type = 'file'
        ad.inputs.mask_file = brain_fmri_file
        ad.inputs.realignment_parameters = 'functional.par'
        ad.inputs.parameter_source = 'FSL'       
        ad.inputs.use_norm = True
        ad.inputs.norm_threshold = 1
        ad.inputs.zintensity_threshold = 3
        ad.run() 

    """
    Remove or replace outlier volumes.
    """
    if correct_outliers:
        # graymatter-masked, motion-corrected data
        cortex_fmri_file = data_path + subject_id + fmri_path + '_cortex' + file_append
        cortex_fmri_no_outliers_file = data_path + subject_id + fmri_path + '_cortex_no_outliers' + file_append

        vol_list = open(stats_path + subject_id + stats_path_end, 'r').readlines()
        vol_list = [int(d)-1 for d in vol_list]
        if len(vol_list) > 0:

            # Load image, replace volumes, and save result
            print('Data path: ' + cortex_fmri_file)
            print('RapidArt output path: ' + stats_path + subject_id + stats_path_end)
            img = nb.load(cortex_fmri_file)
            data = img.get_data()

            if remove_volumes:
                keep_vol_list = [k for k in range(data.shape[-1]) if k not in vol_list]
                data2 = np.float64(data[:,:,:,keep_vol_list])
            else:
                data2 = np.float64(data)
                for k in vol_list:
                    data2[:,:,:,k] = (data[:,:,:,k] * 0) - 1

            print('Output file: ' + cortex_fmri_no_outliers_file)
            img2 = nb.Nifti1Image(data2,np.eye(4))
            nb.save(img2,cortex_fmri_no_outliers_file)
