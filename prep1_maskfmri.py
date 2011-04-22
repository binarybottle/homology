"""
Preprocess functional data to extract activity in gray matter.

1. Realign each functional run to its mean volume.
2. Register the mean functional image to the corresponding FreeSurfer structural data.
3. Inverse transform the FreeSurfer gray matter to the mean functional image.
4. Mask each functional image in the time series with the gray matter mask.
5. Find motion and intensity outliers.

Programs: FSL and FreeSurfer

1. mcflirt:     get realigned + mean time series
2. bbregister:  register mean to FreeSurfer
3. mri_vol2vol: transform gray matter ([lh,rh].ribbon.mgz) to mean
   mri_vol2vol: transform brainmask (aseg.mgz) to mean (for rapidart)
4. mri_mask:    mask functionals with gray matter
5. rapidart:    find outliers

(c) Arno Klein  .  arno@binarybottle.com  .  2011  .  MIT license
"""

motioncorrect_fmri = 0
register_fmri2mri = 0
transform_mri2fmri = 0
mask_fmri = 1
detect_artifacts = 0

import os
from subprocess import call
#import glob
#import numpy as np
#import nibabel

from settings import data_path, fmri_path, file_append #, label_path, label_path_end

for subject_id in os.listdir(data_path):  #glob.glob(func_path):
  if subject_id == 'sub01912':

    """
    Realign each functional run to its mean volume.
    ... mcflirt -in <fmri file> -out <output file> -meanvol'
    """
    moco_command = 'mcflirt'
    fmri_file = data_path + subject_id + fmri_path + file_append
    moco_file_stem = data_path + subject_id + fmri_path + '_' + moco_command
    moco_file = moco_file_stem + file_append
    if motioncorrect_fmri:
        args = ' '.join([moco_command, '-in', fmri_file, '-out', moco_file_stem, '-meanvol'])
        print(args); call(args, shell=True)

    """
    Register the mean functional image to the corresponding FreeSurfer structural data.
    ... bbregister --s <subject> --mov <fmri file> --init-fsl --reg register.dat --t2
    """
    reg_command = 'bbregister'
    mean_fmri_file = data_path + subject_id + fmri_path + '_' + moco_command + '_mean_reg' + file_append
    reg_xfm_file = data_path + subject_id + fmri_path + '_' + moco_command + '_' + reg_command + '.dat'
    if register_fmri2mri:
        args = ' '.join([reg_command,'--s',subject_id,'--mov',mean_fmri_file, '--reg',reg_xfm_file, '--init-fsl --t2'])
        print(args); call(args, shell=True)

    """
    Inverse transform the FreeSurfer cortical gray matter ribbon to the mean functional image.
    ... mri_vol2vol --s <subject> --fstarg ribbon.mgz --mov <mean fmri> --inv --reg <bbregister xfm> --nearest --o <output>
    """
    xfm_command = 'mri_vol2vol'
    rh_ribbon2fmri_file = data_path + subject_id + fmri_path + '_' + moco_command + '_' + reg_command + '_rh.ribbon_mask' + file_append
    lh_ribbon2fmri_file = data_path + subject_id + fmri_path + '_' + moco_command + '_' + reg_command + '_lh.ribbon_mask' + file_append
    aseg2fmri_file = data_path + subject_id + fmri_path + '_' + moco_command + '_' + reg_command + '_aseg' + file_append
    if transform_mri2fmri:
        args = ' '.join([xfm_command, '--s', subject_id, '--fstarg aseg.mgz', '--mov', mean_fmri_file, '--inv --reg', reg_xfm_file, '--nearest','--o', aseg2fmri_file])
        print(args); call(args, shell=True)
        args = ' '.join([xfm_command, '--s', subject_id, '--fstarg rh.ribbon.mgz', '--mov', mean_fmri_file, '--inv --reg', reg_xfm_file, '--nearest','--o', rh_ribbon2fmri_file])
        print(args); call(args, shell=True)
        args = ' '.join([xfm_command, '--s', subject_id, '--fstarg lh.ribbon.mgz', '--mov', mean_fmri_file, '--inv --reg', reg_xfm_file, '--nearest','--o', lh_ribbon2fmri_file])
        print(args); call(args, shell=True)

    """
    Mask each functional image in the time series with the gray matter mask.
    ... mri_mask <fmri> <ribbons> <output>
    """
    mask_command = 'mri_mask'
    rh_masked_fmri_file = data_path + subject_id + fmri_path + '_rh_masked' + file_append
    lh_masked_fmri_file = data_path + subject_id + fmri_path + '_lh_masked' + file_append
    if mask_fmri:
        args = ' '.join([mask_command, fmri_file, rh_ribbon2fmri_file, rh_masked_fmri_file])
        print(args); call(args, shell=True)
        args = ' '.join([mask_command, fmri_file, rh_ribbon2fmri_file, lh_masked_fmri_file])
        print(args); call(args, shell=True)

    """
    Find motion and intensity outliers.
    ... ???rapidart
    """
    xfm_command = 'mri_vol2vol'
    rh_ribbon2fmri_file = data_path + subject_id + fmri_path + '_' + moco_command + '_' + reg_command + '_rh.ribbon' + file_append
    lh_ribbon2fmri_file = data_path + subject_id + fmri_path + '_' + moco_command + '_' + reg_command + '_lh.ribbon' + file_append
    aseg2fmri_file = data_path + subject_id + fmri_path + '_' + moco_command + '_' + reg_command + '_aseg' + file_append
    if detect_artifacts:
        args = ' '.join([xfm_command, '--s', subject_id, '--fstarg aseg.mgz', '--mov', mean_fmri_file, '--inv --reg', reg_xfm_file, '--nearest','--o', aseg2fmri_file])
        print(args); call(args, shell=True)



        #args = ['rm',data_path + subject_id + fmri_path + '_' + moco_command + '_mean_reg.nii.gz']


