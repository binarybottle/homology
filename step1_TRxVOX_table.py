#!/usr/bin/python
import os,sys,warnings,glob
warnings.simplefilter('ignore')
from nibabel import load
import numpy as np

global base_path,out_path
base_path = '/projects/topology_2010/'
adhd = 0
if adhd:
  out_path = base_path + 'output/tables/adhd/'
  subject_path = base_path + 'preproc/output/adhd/'
else:
  out_path = base_path + 'output/tables/controls/'
  subject_path = base_path + 'preproc/output/controls/'
subject_path_end = '/functional/rest_preprocessed_gray_noIntensityOutliers.nii.gz'
subject_path_end2 = '/functional/rest_preprocessed_gray.nii.gz'

if __name__ == '__main__':
	"""
	This program outputs 1 csv file per subject, 
	where each row is a voxel and columns are fMRI TRs.
	"""
	# Iterate over subjects
	for subject in glob.glob(subject_path + "*"):
		subject_id = subject.split("/")[-1]
		print subject_id

		# Set up the csv file for the subject
		f = open(out_path + subject_id + "_VOXvsTR.csv","w")

		# Iterate over TRs in the subject's image
		if os.path.exists(subject_path + subject_id + subject_path_end):
  		  img = load(subject_path + subject_id + subject_path_end)
		elif os.path.exists(subject_path + subject_id + subject_path_end2):
  		  img = load(subject_path + subject_id + subject_path_end2)
		data = img.get_data()
		for ivol in range(data.shape[-1]):
			f.writelines(','.join([str(s) for s in data[:,:,:,ivol].ravel()]) + '\n')
			print("  TR " + str(ivol))
		
		f.close()
		