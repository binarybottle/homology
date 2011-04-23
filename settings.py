"""
Settings for the entire fMRI+topology processing pipeline

(c) Arno Klein  .  arno@binarybottle.com  .  2011  .  MIT license
"""

from subprocess import call

freesurfer_home = '/Applications/freesurfer'
subjects_dir = '/hd2/data/Brains/FunctionalConnectomes1000/NewYork_freesurfer_subjects/fs_output'

# prep1_maskfmri.py:
data_path = '/hd2/data/Brains/FunctionalConnectomes1000/NewYork_a_ADHD_part1/'
fmri_path = '/func/rest'
file_append = '.nii.gz'
moco_command = 'mcflirt'
reg_command = 'bbregister'

# prep2_outliers.py:  data_path, fmri_path, file_append, moco_command
stats_path = './preproc/output/'
stats_path_end = '/art/art.rest_preprocessed.nii_outliers.txt' 
remove_volumes = 0

# prep3_ROIsurf2vol:  data_path, moco_command
anat_path = '/anat/mprage_anonymized'

# step1_ROIxTR_table:
# label_path, labelfunc_path_end, preproc_func_path, preproc_func_path_end
#patient = 1
#if patient:
#    preproc_func_path = data_path + 'NewYork_a_ADHD/'
#else:
#    preproc_func_path = data_path + 'NewYork_a_part1/'
label_list = '/projects/homology/region_nums_names.txt'
table_path = '/projects/homology/output/tables/ROIxTR/'
table_end = '_ROIvsTR.csv'

# step2_binarize_table:
# table_path, table_end
binary_table_path = './output/tables/ROIxTR_binary/Binary_for_sub'

# step3_filter:
# binary_table_path
binary_table_path2 = './output/tables/ROIxTR_binary_nconcurrences/'
binary_table_end = ''
binary_table_end2 = '_nconcurrences.txt'
first_column = 0 # 0-based


# step4_persistence:
# binary_table_path, binary_table_path2, binary_table_end, binary_table_end2, first_column
kskeleton = 3  # A k-simplex has k+1 vertices (for Dionysus)
reverse_filtration_order = 1
persistence_type = 3  # static_persistence = 1; dynamic_persistence = 2; nmfsimtop = 3
remove_dimension1 = 1
output_table_path = './output/tables/'



args1 = 'FREESURFER_HOME=' + freesurfer_home
args2 = 'SUBJECTS_DIR=' + subjects_dir
args3 = 'export FREESURFER_HOME SUBJECTS_DIR'
print(args1); call(args1, shell=True)
print(args2); call(args2, shell=True)
print(args3); call(args3, shell=True)
