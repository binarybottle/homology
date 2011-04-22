"""
 Settings for the entire topology processing pipeline

(c) Arno Klein  .  arno@binarybottle.com  .  2011

so take the mean functional after realignment, 
and bbregister it to the freesurfer subject. 
this will give you a registration matrix (.dat file). 
then apply mri_vol2vol with the inverse option to convert 
freesurfer volume labels to functional space with nearest neighbor interpolation. 

mcflirt -> to get realigned + mean time series
bbregister -> mean to freesurfer
vol2vol -> aseg.mgz : brainmask for rapidart
vol2vol -> ribbon.mgz : gray ribbon for masking functionals
rapidart -> to get outliers

"""
import os
from glob import glob

# prep0_coregister:
data_path = '/hd2/data/Brains/FunctionalConnectomes1000/NewYork_a_ADHD_part1/'
fmri_path = '/func/rest'
file_append = '.nii.gz'
#xfm_path = func_path
#xfm_path_end = "/coregister/mprage_anonymized_brain_flirt.mat"
label_path = data_path + 'NewYork_freesurfer_labels/'
label_path_end = '_labels.nii.gz'
labelfunc_path_end = '_labels_funcspace.nii.gz'

# prep1_nipype (Nipype):
datasource_inputs = 'NewYork_a_*/%s/%s/%s.nii.gz'
patient_subject_list = [path.split('/')[-1] for path in glob(os.path.join(data_path,'NewYork_a_ADHD/sub*'))]
control_subject_list = [path.split('/')[-1] for path in glob(os.path.join(data_path,'NewYork_a_part1/sub*'))]
subject_list = patient_subject_list + control_subject_list

# prep2_intensity_outliers:
preproc_func = '/functional/rest_preprocessed_gray.nii.gz'
preproc_func_path_end = '/rest_preprocessed_gray_negativeIntensityOutliers.nii.gz'

# prep3_ROIsurf2vol:
# data_path

# prep4_ROI2func:
#?label_path = data_path + 'NewYork_freesurfer_labels/'
#?label_path_end = '_labels.nii.gz'
#?labelfunc_path_end = '_labels_funcspace.nii.gz'
#?func_path = '/projects/homology/preproc/workingdir/level1/preproc/_subject_id_'
#?func_path_end = '/realign/rest_dtype_mcf.nii.gz'
#?xfm_path = func_path
#?xfm_path_end = "/coregister/mprage_anonymized_brain_flirt.mat"

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
