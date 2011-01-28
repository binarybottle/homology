"""
Use FreeSurfer utilities to propagate surface labels through cortical gray matter.

(c) Arno Klein  .  arno@binarybottle.com  .  2010
"""

import os, sys, glob
from settings.py import *

fs_output_dir = "./output/freesurfer/"
ref_path1 = data_path + "NewYork_a_ADHD/"
ref_path2 = data_path + "NewYork_a_part1/"
ref_end = '/anat/mprage_anonymized.nii.gz'

cmd = 'SUBJECTS_DIR=' + fs_output_dir
print(cmd); os.system(cmd)
cmd = 'export SUBJECTS_DIR'
print(cmd); os.system(cmd)

for subject_path in glob.glob(fs_output_dir + "*"):

  subject = subject_path.split("/")[-1]
  test_file = subject_path + '/label/rh.cortex.label'

  if os.path.exists(test_file):
    ref_file = ref_path1 + subject + ref_end
    if os.path.exists(ref_file):
      pass
    else:
      ref_file = ref_path2 + subject + ref_end
    if os.path.exists(ref_file):
      out_file2 = out_path + subject + '_labels.nii.gz'
      if os.path.exists(out_file2):
        pass
      else:
        out_file1 = out_path + subject + '_aparc2aseg.nii.gz'
        cmd = 'mri_aparc2aseg --s ' + subject + ' --o ' + out_file1
        print(cmd); os.system(cmd)

        cmd = 'mri_convert ' + out_file1 + ' ' + out_file2 + ' -rl ' + ref_file + ' -ns 1 -nc -rt nearest'
        print(cmd); os.system(cmd)
