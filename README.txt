-------------------------
step1_fslabels_to_fmri.py
-------------------------
Preprocess functional data to extract activity in gray matter.

1. Realign each functional run to its mean volume.
2. Register the mean functional image to the corresponding FreeSurfer structural data.
3. Inverse transform the FreeSurfer labels to the mean functional image.
4. Mask each functional image in the time series with the brain mask.

Programs: FSL, FreeSurfer

1. mcflirt:        get realigned + mean time series
2. bbregister:     register mean to FreeSurfer
3. mri_aparc2aseg: map cortical labels to the segmentation volume
   mri_vol2vol:    transform labels to fmri data
4. mri_mask:       mask functionals with the brain mask

-----------------
step2_activity.py
-----------------
Prepare table of average activity per labeled region.

This program outputs 1 table file per subject,
where each row is a region and columns are time points (e.g., fMRI TRs).
The first column contains the label indices.

Calls label_list = '/projects/homology/region_nums_names.txt'

---------------
step3_filter.py
---------------
1. Detrend activity for each region (table row).
2. Denoise activity for each region by number of median absolute deviations from the median.
3. Bandlimit the frequencies of activity for each region.

thresh_deviations = 5
TR = 2
freq_lower = 0.0
freq_upper = 0.10

---------------
step4_binary.py
---------------
1. Remove rows of a table file with least variation (interquartile range over median).
2. Binarize the remaining rows, with a 1 indicating high activity.

min_percentile_variation = 20
min_percentile_activity = 80

---------------------
step5_concurrences.py
---------------------
Run frequency filtration on a binary table.

Filter the table by the number of times (frequency) that the active regions 
of a given column are repeated as a subset of the active regions of the other columns.
The complex at frequency level f includes all concurrences that happen at least f times.

Calls detrendR.py:
R code for robust detrending of data. (c) Steve Ellis

--------------------
step6_persistence.py
--------------------
Compute persistence from a binary table of activity data.

Persistence code was developed by Dmitriy Morozov (Dionysus) and Vidit Nanda (nmfsimtop).

kskeleton = 3  # A k-simplex has k+1 vertices (for Dionysus)
reverse_filtration_order = 1
persistence_type = 2  # static_persistence = 1; dynamic_persistence = 2; nmfsimtop = 3
remove_dimension1 = 1
