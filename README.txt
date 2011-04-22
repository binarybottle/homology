"""
Use FSL's mcflirt to register fMRI data to middle image of first run.

mcflirt -> to get realigned + mean time series
bbregister -> mean to freesurfer
vol2vol -> aseg.mgz : brainmask for rapidart
vol2vol -> ribbon.mgz : gray ribbon for masking functionals
rapidart -> to get outliers


(c) Arno Klein  .  arno@binarybottle.com  .  2011
"""

import os,sys,warnings,glob

from settings import func_path, func_path_end, xfm_path, xfm_path_end

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
