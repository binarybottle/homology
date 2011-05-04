README file for the fMRI topology project (@rno klein, 12/2009)

Objective: 

    Determine whether fMRI data (representing different task conditions)
    may be distinguished from one another using algebraic topology.

    Specifically, we will compare simplicial complexes formed by concurrent 
    BOLD activity across brain regions, in the same manner that such complexes 
    constructed from simulated hippocampal place cell activity were compared in:

    Carina Curto and Vladimir Itsov, "Cell Groups Reveal Structure of Stimulus Space" 
    PLoS Computational Biology, Oct. 2008.

Data:

   The fBIRN Traveling Subject 2003 dataset (http://www.birncommunity.org/resources/data/)
   was chosen because it is publicly available and has T1-weighted data for 4 subjects,
   as well as fMRI data for 10 tasks (in 4 categories) acquired repeatedly
   from multiple scanners from multiple institutions.
   For this pilot experiment, we will try to distinguish between different
   task conditions in the same subject acquired from the same scanner. 

   The AAL brain atlas (Tzourio-Mazoyer et al., 2002) was chosen to label 
   the functional data because it is publicly available and has over 100 
   anatomically labeled regions that are considered functionally relevant.

Software:

   FSL (brain extraction, linear registration):  http://www.fmrib.ox.ac.uk/fsl/
   ANTS (nonlinear registration):  http://picsl.upenn.edu/ANTS/
   custom Python code (building the tables)
   
Methods:

1. We extracted the brain from the subject's T1-weighted image using FSL's bet2 command
   (visibly inspected and approved).

2. We registered the brain to the (already motion-corrected) EPI BOLD data 
   acquired from the same subject (12-dof affine transform, using FSL's flirt command,
   visibly inspected and approved).

3. We flipped the Colin27 single-subject MRI brain template and the AAL atlas 
   and altered their headers (using ANTS's ImageMath):
   
   ImageMath 3 /piece-of-mind/data/Atlases/AAL_Colin27/single_subj_T1_brain_1mm_flip_fixed.nii.gz \
          CompareHeadersAndImages \
          /piece-of-mind/projects/topology_200912/fBIRN_UCI1_data/s1/T1_bet2/f0001_bet2_flip.nii.gz \
          /piece-of-mind/data/Atlases/AAL_Colin27/single_subj_T1_brain_1mm_flip.nii.gz

   ImageMath 3 /piece-of-mind/data/Atlases/AAL_Colin27/aal_trans_flip_fixed.nii.gz \
          CompareHeadersAndImages \
          /piece-of-mind/data/Atlases/AAL_Colin27/single_subj_T1_brain_1mm_flip.nii.gz \
          /piece-of-mind/data/Atlases/AAL_Colin27/aal_trans_flip.nii.gz
   (NOTE: made x value positive in the header:)
   fsledithd /piece-of-mind/data/Atlases/AAL_Colin27/aal_trans_flip_fixed.nii.gz emacs

4. We put the AAL brain atlas labels in the same space as the subject's fMRI data
   in the following manner:

   Output from #3 was registered to the brain in #2, using 
   SyN nonlinear diffeomorphic registration from the ANTS software package.
   The nonlinear transform was then applied to the (flipped) AAL brain atlas
   (which was already registered to the original Colin27 brain input for #3). 
   (Results were visibly inspected.)
 
   sh ants.sh 3 /piece-of-mind/projects/topology_200912/fBIRN_UCI1_data/s1/T1_bet2/f0001_bet2_flip.nii.gz \
                /piece-of-mind/data/Atlases/AAL_Colin27/single_subj_T1_brain_1mm_flip_fixed.nii.gz \
                colin27_to_s1_ 30x99x11 \
                /piece-of-mind/data/Atlases/AAL_Colin27/aal_trans_flip.nii.gz
                [NOTE: last argument didn't work, so we ran the WarpImage... command below)

   The ants.sh parameters were altered to match those used in (Klein, et al. 2009):

       ANTS 3 -m PR[/piece-of-mind/projects/topology_200912/fBIRN_UCI1_data/s1/T1_bet2/f0001_bet2_flip_fixed.nii.gz, \
                    /piece-of-mind/data/Atlases/AAL_Colin27/single_subj_T1_brain_1mm_flip.hdr, 1, 2] \
              -o /piece-of-mind/projects/topology_200912/fBIRN_UCI1_data/s1/colin27_to_s1.nii.gz \
              -r Gauss[2,0] -t SyN[0.5] -i 30x99x11 --use-Histogram-Matching

       WarpImageMultiTransform 3 /piece-of-mind/data/Atlases/AAL_Colin27/aal_trans_flip.nii.gz \
              /piece-of-mind/projects/topology_200912/fBIRN_UCI1_data/s1/aal_to_s1.nii.gz \
              -R /piece-of-mind/projects/topology_200912/fBIRN_UCI1_data/s1/T1_bet2/f0001_bet2_flip.nii.gz \
              colin27_to_s1_Warp.nii colin27_to_s1_Affine.txt --use-NN 

5. We used a custom Python program to create a table for each task condition for the subject,
   with each row corresponding to a brain region and each column corresponding to a time point.

