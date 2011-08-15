-------------------------
step1_fslabels_to_fmri.py
-------------------------
Preprocess functional data to extract activity in gray matter.

1. Register the mean functional image to the corresponding FreeSurfer structural data.
2. Inverse transform the FreeSurfer labels to the mean functional image.
3. Mask each functional image in the time series with the brain mask.

Programs: FSL, FreeSurfer

1. bbregister:     register mean to FreeSurfer
2. mri_aparc2aseg: map cortical labels to the segmentation volume
   mri_vol2vol:    transform labels to fmri data
3. mri_mask:       mask functionals with the brain mask

-----------------
step2_activity.py
-----------------
Prepare table of average activity per labeled region.

This program outputs 1 table file per subject,
where each row is a region and columns are time points (e.g., fMRI TRs).
The first column contains the label indices.

Calls label_list = '/projects/homology/region_nums_names.txt'
