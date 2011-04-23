#!/usr/bin/python
"""
Preprocess functional data to extract activity in gray matter.

1. Realign each functional run to its mean volume.
2. Register the mean functional image to the corresponding FreeSurfer structural data.
3. Inverse transform the FreeSurfer labels to the mean functional image.
#4. Mask each functional image in the time series with the gray matter mask.
#5. Transform FreeSurfer labels to the mean functional image.

Programs: FSL, FreeSurfer

1. mcflirt:        get realigned + mean time series
2. bbregister:     register mean to FreeSurfer
3. mri_aparc2aseg: map cortical labels to the segmentation volume
   mri_vol2vol:    transform labels to fmri data
#3. mri_vol2vol:    transform gray matter ([lh,rh].ribbon.mgz) to mean
#   mri_vol2vol:    transform brainmask (aseg.mgz) to mean (for rapidart)
#4. mri_mask:       mask functionals with gray matter

(c) Arno Klein  .  arno@binarybottle.com  .  2011  .  MIT license
"""

motioncorrect_fmri = 1
register_fmri2mri = 1
transform_labels2fmri = 1
#transform_mri2fmri = 0
#mask_fmri = 1

freesurfer_home = '/Applications/freesurfer'
subjects_dir = '/hd2/data/Brains/FunctionalConnectomes1000/NewYork_freesurfer_subjects/fs_output'
data_path = '/hd2/data/Brains/FunctionalConnectomes1000/NewYork_a_ADHD_part1/'
fmri_path = '/func/rest'
anat_path = '/anat/mprage_anonymized'
file_append = '.nii.gz'
moco_command = 'mcflirt'
reg_command = 'bbregister'

import os
from subprocess import call

for subject_id in os.listdir(data_path):
  if subject_id == 'sub01912':

    """
    Realign each functional run to its mean volume.
    ... mcflirt -in <fmri file> -out <output file> -meanvol -plots' (-plots: rapidart requires .par file)
    """
    fmri_file = data_path + subject_id + fmri_path + file_append
    moco_file_stem = data_path + subject_id + fmri_path + '_' + moco_command
    if motioncorrect_fmri:
        args = [moco_command, '-in', fmri_file, '-out', moco_file_stem, '-meanvol'] # -plots -stats -mats']
        print(' '.join(args)); call(' '.join(args), shell=True)

    """
    Register the mean functional image to the corresponding FreeSurfer structural data.
    ... bbregister --s <subject> --mov <mean fmri file> --init-fsl --reg register.dat --t2
    """
    mean_fmri_file = data_path + subject_id + fmri_path + '_' + moco_command + '_mean_reg' + file_append
    reg_xfm_file = data_path + subject_id + fmri_path + '_' + moco_command + '_' + reg_command + '.dat'
    if register_fmri2mri:
        args = [reg_command,'--s',subject_id,'--mov',mean_fmri_file, '--reg',reg_xfm_file, '--init-fsl --t2']
        print(' '.join(args)); call(' '.join(args), shell=True)

    """
    Inverse transform the FreeSurfer label data to the mean functional image.
    ... mri_vol2vol --s <subject> --fstarg <fs volume> --mov <mean fmri> --inv --reg <bbregister xfm> --nearest --o <output>
    """
#    anat_file = anat_path + file_append
    labeled_mri_file = data_path + subject_id + anat_path + '_aparc2aseg' + file_append
    aseg2fmri_file = data_path + subject_id + fmri_path + '_aseg' + file_append
    if transform_labels2fmri:
        args1 = ['mri_aparc2aseg', '--s', subject_id, '--o', labeled_mri]
#        args2 = ['mri_convert', labeled_mri, labeled_mri2, '-rl', anat_file, '-ns 1 -nc -rt nearest']
        args2 = ['mri_vol2vol', '--targ', labeled_mri_file, '--mov', mean_fmri_file, '--inv --reg', reg_xfm_file, '--nearest','--o', labeled_fmri_file]
        args3 = ['mri_vol2vol', '--s', subject_id, '--fstarg aseg.mgz', '--mov', mean_fmri_file, '--inv --reg', reg_xfm_file, '--nearest','--o', aseg2fmri_file]
        print(' '.join(args1)); call(' '.join(args1), shell=True)
        print(' '.join(args2)); call(' '.join(args2), shell=True)
        print(' '.join(args3)); call(' '.join(args3), shell=True)

"""

    Mask each functional image in the time series with the brain mask.
    ... mri_mask <fmri> <mask> <output>

    rh_cortex_fmri_file = data_path + subject_id + fmri_path + '_cortex_rh' + file_append
    lh_cortex_fmri_file = data_path + subject_id + fmri_path + '_cortex_lh' + file_append
    cortex_fmri_file = data_path + subject_id + fmri_path + '_cortex' + file_append
    brain_fmri_file = data_path + subject_id + fmri_path + '_brain' + file_append
    if mask_fmri:
        args1 = ['mri_mask', fmri_file, rh_ribbon2fmri_file, rh_cortex_fmri_file]
        args2 = ['mri_mask', fmri_file, lh_ribbon2fmri_file, lh_cortex_fmri_file]
        args3 = ['fslmaths', rh_cortex_fmri_file, '-add', lh_cortex_fmri_file, cortex_fmri_file]
        args4 = ['fslmaths', aseg2fmri_file, '-bin', brain_fmri_file]
        print(' '.join(args1)); call(' '.join(args1), shell=True)
        print(' '.join(args2)); call(' '.join(args2), shell=True)
        print(' '.join(args3)); call(' '.join(args3), shell=True)
        print(' '.join(args4)); call(' '.join(args4), shell=True)

    Inverse transform the FreeSurfer label data to the mean functional image.
    ... mri_vol2vol --s <subject> --fstarg <fs volume> --mov <mean fmri> --inv --reg <bbregister xfm> --nearest --o <output>

    rh_ribbon2fmri_file = data_path + subject_id + fmri_path + '_' + moco_command + '_' + reg_command + '_rh.ribbon_mask' + file_append
    lh_ribbon2fmri_file = data_path + subject_id + fmri_path + '_' + moco_command + '_' + reg_command + '_lh.ribbon_mask' + file_append
    aseg2fmri_file = data_path + subject_id + fmri_path + '_' + moco_command + '_' + reg_command + '_aseg' + file_append
    if transform_labels2fmri:
        anat_file = anat_path + file_append
        labeled_volume = data_path + subject_id + anat_path + '_aparc2aseg' + file_append
        reg_xfm_file = data_path + subject_id + fmri_path + '_' + moco_command + '_' + reg_command + '.dat'
        mean_fmri_file = data_path + subject_id + fmri_path + '_' + moco_command + '_mean_reg' + file_append
        labeled_fmri_file = data_path + subject_id + fmri_path + '_labels' + file_append

        args1 = ['mri_aparc2aseg', '--s', subject_id, '--o', labeled_volume]
        args2 = ['mri_vol2vol', '--targ', labeled_volume, '--mov', mean_fmri_file, '--inv --reg', reg_xfm_file, '--nearest','--o', labeled_fmri_file]
       #args2 = ['mri_convert', labeled_volume1, labeled_volume2, '-rl', anat_file, '-ns 1 -nc -rt nearest']

        print(' '.join(args1)); call(' '.join(args1), shell=True)
        print(' '.join(args2)); call(' '.join(args2), shell=True)
"""