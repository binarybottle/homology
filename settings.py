"""
 Settings for the entire topology processing pipeline

(c) Arno Klein  .  arno@binarybottle.com  .  2010
"""
import os
from glob import glob

data_path = '/hd2/data/Brains/FunctionalConnectomes1000/'

# prep1_nipype (Nipype):
datasource_inputs = 'NewYork_a_*/%s/%s/%s.nii.gz'
patient_subject_list = [path.split('/')[-1] for path in glob(os.path.join(data_path,'NewYork_a_ADHD/sub*'))]
control_subject_list = [path.split('/')[-1] for path in glob(os.path.join(data_path,'NewYork_a_part1/sub*'))]
subject_list = patient_subject_list + control_subject_list

# prep2_intensity_outliers:
# N/A

# prep3_ROIsurf2vol:
# data_path

# prep4_ROI2func:
label_path = data_path + 'NewYork_freesurfer_labels/'
label_path_end = '_labels.nii.gz'
labelfunc_path_end = '_labels_funcspace.nii.gz'
func_path = '/projects/topology_2010/preproc/workingdir/level1/preproc/_subject_id_'
func_path_end = '/realign/rest_dtype_mcf.nii.gz'

# step1_ROIxTR_table:
# label_path, labelfunc_path_end, func_path, func_path_end
label_list = '/projects/topology_2010/region_nums_names.txt'
table_path = '/projects/topology_2010/output/tables/ROIxTR/'
table_end = '_ROIvsTR.csv'

# step2_binarize_table:
# table_path, table_end
binary_table_path = './output/tables/ROIxTR_binary/'

# step3_filter:
# binary_table_path
binary_table_path2 = './output/tables/ROIxTR_binary_nconcurrences/'
binary_table_end = 'ROIvsTR_binary.csv'
binary_table_end2 = '_nconcurrences.txt'

# step4_persistence:
# binary_table_path, binary_table_path2, binary_table_end, binary_table_end2