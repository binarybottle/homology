#!/usr/bin/python
"""
Preprocess functional data to extract activity in gray matter.

1. Realign each functional run to its mean volume.
2. Correct for sampling offsets inherent in slice-wise EPI acquisition sequences.
3. Register the mean functional image to the corresponding FreeSurfer structural data.
4. Inverse transform the FreeSurfer labels to the mean functional image.
5. Mask each functional image in the time series with the brain mask.

Programs: FSL, FreeSurfer

1. mcflirt:        get realigned + mean time series
2. slicetimer:     slice-time correction (ascending, interleaved)
3. bbregister:     register mean to FreeSurfer
4. mri_aparc2aseg: map cortical labels to the segmentation volume
   mri_vol2vol:    transform labels to fmri data
5. mri_mask:       mask functionals with the brain mask

(c) Arno Klein  .  arno@binarybottle.com  .  2011  .  MIT license
"""

register_fmri2mri = 1
transform_labels2fmri = 1

freesurfer_home = '/Applications/freesurfer'
subjects_dir = '/hd2/data/Brains/FunctionalConnectomes1000/NewYork_freesurfer_subjects'
data_path = '/hd2/data/Brains/FunctionalConnectomes1000/NewYork_a_ADHD_part1/'
fmri_path = '/func/rest'
anat_path = '/anat/mprage_anonymized'
file_append = '.nii.gz'
moco_command = 'mcflirt'
slicetime_command = 'slicetimer'
reg_command = 'bbregister'

import os
from subprocess import call

debug_run1 = 0

if __name__ == '__main__':

    args1 = 'FREESURFER_HOME=' + freesurfer_home
    args2 = 'SUBJECTS_DIR=' + subjects_dir
    args3 = 'export FREESURFER_HOME SUBJECTS_DIR'
    print(args1); call(args1, shell=True)
    print(args2); call(args2, shell=True)
    print(args3); call(args3, shell=True)

    for subject_id in os.listdir(data_path):

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
        labeled_mri_file = data_path + subject_id + anat_path + '_aparc2aseg' + file_append
        labeled_fmri_file = data_path + subject_id + fmri_path + '_aparc2aseg' + file_append
        aseg2fmri_file = data_path + subject_id + fmri_path + '_aseg' + file_append
        if transform_labels2fmri:
            args1 = ['mri_aparc2aseg', '--s', subject_id, '--o', labeled_mri_file]
            args2 = ['mri_vol2vol', '--targ', labeled_mri_file, '--mov', mean_fmri_file, '--inv --reg', reg_xfm_file, '--nearest','--o', labeled_fmri_file]
            args3 = ['mri_vol2vol', '--s', subject_id, '--fstarg aseg.mgz', '--mov', mean_fmri_file, '--inv --reg', reg_xfm_file, '--nearest','--o', aseg2fmri_file]
            print(' '.join(args1)); call(' '.join(args1), shell=True)
            print(' '.join(args2)); call(' '.join(args2), shell=True)
            print(' '.join(args3)); call(' '.join(args3), shell=True)
