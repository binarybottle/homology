"""
Use FSL's flirt to register labeled cortex to activity data.

(c) Arno Klein  .  arno@binarybottle.com  .  2010
"""

import os,sys,warnings,glob

from settings import func_path, func_path_end, label_path, label_path_end, labelfunc_path_end

func_path = './preproc/workingdir/level1/preproc/_subject_id_'
func_path_end = '/realign/rest_dtype_mcf.nii.gz'
xfm_path = func_path
xfm_path_end = "/coregister/mprage_anonymized_brain_flirt.mat"

for subject_path in glob.glob(label_path + "*" + label_path_end):
	subject_id = subject_path.split(label_path)[-1].split(label_path_end)[0]
	print subject_id

    label_file = label_path + subject_id + label_path_end
    xfm_file = xfm_path + subject_id + xfm_path_end
	func_file = func_path + subject_id + func_path_end
    out_file = label_path + subject_id + labelfunc_path_end

    if os.path.exists(out_file):
		pass
	else:
		cmd = 'flirt -in ' + label_file + ' -ref ' + func_file + ' -applyxfm -init ' + xfm_file + ' -out ' + out_file + ' -interp nearestneighbour'
		print(cmd); os.system(cmd)