"""
First preparation step for the brain activity homology project.

NOTE:  See "Experiment-specific components" below. 
This script preprocesses patient and control subjects
(NYU data on NITRC's Functional Connectome 1000).

Input: patient and control data directory paths

The steps are motion correction, rapidart artifact detection, 
and coregistration and gray matter masking of fMRI data.

(c) Arno Klein and Satrajit S. Ghosh  .  arno@binarybottle.com  .  2010
"""

"""
Tell python where to find the appropriate functions.
"""
from glob import glob
import os                                    # system functions

from nibabel import load
import nipype.interfaces.io as nio           # Data i/o
import nipype.interfaces.fsl as fsl          # fsl
import nipype.interfaces.utility as util     # utility
import nipype.pipeline.engine as pe          # pypeline engine
import nipype.algorithms.rapidart as ra      # artifact detection

from settings import data_path

# Specify the subject directories
patient_subject_list = [path.split('/')[-1] for path in glob(os.path.join(data_path,'NewYork_a_ADHD/sub*'))]
control_subject_list = [path.split('/')[-1] for path in glob(os.path.join(data_path,'NewYork_a_part1/sub*'))]
subject_list = patient_subject_list + control_subject_list

#####################################################################
# Preliminaries

"""
Set up any package-specific configuration. The output file format
for FSL routines is being set to uncompressed NIFTI.
"""
# Tell fsl to generate all output in compressed nifti format
print fsl.Info.version()
fsl.FSLCommand.set_default_output_type('NIFTI_GZ')

"""
Setup preprocessing workflow
----------------------------

These are the first steps of a generic fsl feat preprocessing workflow 
encompassing skull stripping and motion.

"""
preproc = pe.Workflow(name='preproc')

"""
Set up a node to define all inputs required for the preprocessing workflow
"""
inputnode = pe.Node(interface=util.IdentityInterface(fields=['func',
                                                             'struct',]),
                    name='inputspec')

"""
Convert functional images to float representation. If there were more than
one functional run we would use a MapNode to convert each run.
"""
img2float = pe.Node(interface=fsl.ImageMaths(out_data_type='float',
                                             op_string = '',
                                             suffix='_dtype'),
                    name='img2float')

"""
Extract the middle volume of the first run as the reference
"""
extract_ref = pe.Node(interface=fsl.ExtractROI(t_size=1),
                      name = 'extractref')

"""
Define a function to pick the [index] file from a list of files
"""
def pickX(files, index=0):
    if isinstance(files, list):
        return files[index]
    else:
        return files

"""
Define a function to return the 1-based index of the middle volume
"""
def getmiddlevolume(func):
    funcfile = func
    if isinstance(func, list):
        funcfile = func[0]
    _,_,_,timepoints = load(funcfile).get_shape()
    return (timepoints/2)-1

"""
Realign the functional runs to the middle volume of the first run.
"""
motion_correct = pe.Node(interface=fsl.MCFLIRT(save_mats = True,
                                               save_plots = True),
                         name='realign')

"""
Extract the mean volume of the first functional run
"""
meanfunc = pe.Node(interface=fsl.ImageMaths(op_string = '-Tmean',
                                            suffix='_mean'),
                   name='meanfunc')

"""
Strip the skull from the mean functional to generate a mask.
"""
meanfuncmask = pe.Node(interface=fsl.BET(mask = True,
                                         no_output=True,
                                         frac = 0.3),
                       name = 'meanfuncmask')

"""
Mask the functional runs with the mask.
"""
maskfunc = pe.Node(interface=fsl.ImageMaths(suffix='_bet',
                                            op_string='-mas'),
                   name = 'maskfunc')

"""
Strip the skull of the structural image and 
coregister the result to the mean functional image
"""
skullstrip = pe.Node(interface=fsl.BET(mask = True),
                     name = 'stripstruct')

coregister = pe.Node(interface=fsl.FLIRT(dof=6),
                     name = 'coregister')

"""
Run FAST on the structural image to obtain the gray matter mask.
"""
segmentstruct = pe.Node(interface=fsl.FAST(no_pve=True,
                                           number_classes=3,
                                           segments=True),
                      name = 'segment')

"""
Apply the registration transform to the gray matter mask.
"""
applyReg2graymask = pe.Node(interface=fsl.ApplyXfm(apply_xfm=True,
                                                   interp='nearestneighbour'),
                           name = 'applyreg2graymask')

"""
Mask the functional runs with the gray matter mask.
"""
maskfuncgray = pe.Node(interface=fsl.ImageMaths(suffix='_gray',
                                            op_string='-mas'),
                   name = 'maskfuncgray')

"""
Use :class:`nipype.algorithms.rapidart` to determine which if any 
images in the functional series are outliers based on deviations 
in intensity and/or movement.
"""
art = pe.Node(interface=ra.ArtifactDetect(use_differences = [True,False],
                                          use_norm = True,
                                          norm_threshold = 1.0,
                                          zintensity_threshold = 3,
                                          parameter_source = 'FSL',
                                          mask_type = 'file'),
              name="art")

"""
Connect all of the nodes.
"""
preproc.connect([(inputnode, img2float, [('func','in_file')]),
                 (img2float, extract_ref, [('out_file', 'in_file'),
                                           (('out_file',getmiddlevolume), 't_min')]),
                 (img2float, motion_correct, [('out_file','in_file')]),
                 (extract_ref, motion_correct, [('roi_file','ref_file')]),
                 (motion_correct, meanfunc, [('out_file','in_file')]),
                 (motion_correct, maskfunc, [('out_file','in_file')]),
                 (meanfunc, meanfuncmask, [('out_file','in_file')]),
                 (meanfuncmask, maskfunc, [('mask_file','in_file2')]),
                 (meanfunc, coregister,[('out_file','reference')]),
                 (skullstrip, coregister,[('out_file','in_file')]),
                 (inputnode, skullstrip,[('struct','in_file')]),
                 (skullstrip, segmentstruct, [('out_file','in_files')]),
                 (segmentstruct, applyReg2graymask, [(('tissue_class_files',pickX,1),'in_file')]),
                 (meanfunc, applyReg2graymask, [('out_file','reference')]),
                 (coregister, applyReg2graymask, [('out_matrix_file','in_matrix_file')]),
                 (maskfunc, maskfuncgray, [('out_file', 'in_file')]),
                 (applyReg2graymask, maskfuncgray, [('out_file', 'in_file2')]),
                 (motion_correct, art, [('par_file','realignment_parameters')]),
                 (maskfunc, art, [('out_file','realigned_files')]),
                 (applyReg2graymask, art, [('out_file', 'mask_file')]),
                 (meanfuncmask, art, [('mask_file', 'mask_file')]),
                 ])


"""
Experiment-specific components
------------------------------

"""
# Map field names to individual subject runs.
info = dict(func=[['subject_id', 'func', 'rest']],
            struct=[['subject_id', 'anat', 'mprage_anonymized']])

infosource = pe.Node(interface=util.IdentityInterface(fields=['subject_id']),
                     name="infosource")

"""Here we set up iteration over all the subjects. The following line
is a particular example of the flexibility of the system.  The
``datasource`` attribute ``iterables`` tells the pipeline engine that
it should repeat the analysis on each of the items in the
``subject_list``. In the current example, the entire first level
preprocessing and estimation will be repeated for each subject
contained in subject_list.
"""

infosource.iterables = ('subject_id', subject_list)

"""
Now we create a :class:`nipype.interfaces.io.DataSource` object and
fill in the information from above about the layout of our data.  The
:class:`nipype.pipeline.NodeWrapper` module wraps the interface object
and provides additional housekeeping and pipeline specific
functionality.
"""

datasource = pe.Node(interface=nio.DataGrabber(infields=['subject_id'],
                                               outfields=['func', 'struct']),
                     name = 'datasource')
datasource.inputs.base_directory = data_path
datasource.inputs.template = 'NewYork_a_*/%s/%s/%s.nii.gz'
datasource.inputs.template_args = info


"""
Set up complete workflow
========================
"""

l1pipeline = pe.Workflow(name= "level1")
l1pipeline.base_dir = os.path.abspath('./preproc/workingdir')
l1pipeline.config = dict(crashdump_dir=os.path.abspath('./preproc/crashdumps'))

l1pipeline.connect([(infosource, datasource, [('subject_id', 'subject_id')]),
                    (datasource, preproc, [('struct','inputspec.struct'),
                                           ('func', 'inputspec.func'),
                                           ]),
                    ])

datasink = pe.Node(interface=nio.DataSink(parameterization=False), name="datasink")
def getbasedir(subject_id):
    if subject_id in patient_subject_list:
        base_dir = os.path.abspath('./preproc/output/patients')
    else:
        base_dir = os.path.abspath('./preproc/output/controls')
    return base_dir

datasink.inputs.substitutions = [('dtype_mcf_bet','preprocessed')]
# store relevant outputs from various stages of the 1st level analysis
l1pipeline.connect([(infosource, datasink, [(('subject_id',getbasedir),
                                               'base_directory'),
                                            ('subject_id','container')]),
                    (preproc, datasink,[('maskfuncgray.out_file','functional'),
                                        ('realign.par_file','motion_parameters'),
                                        ('segment.tissue_class_files','segmentation'),
                                        ('art.outlier_files','art.@outliers'),
                                        ('art.statistic_files','art.@stats'),
                                        ])
                    ])

"""
Execute the pipeline
--------------------

The code discussed above sets up all the necessary data structures with
appropriate parameters and the connectivity between the processes, but does not
generate any output. To actually run the analysis on the data the
``nipype.pipeline.engine.Pipeline.Run`` function needs to be called.
"""

if __name__ == '__main__':
    l1pipeline.run()
    l1pipeline.write_graph(graph2use='flat')
