"""
Group files in separate directories.

"""

import sys, os
from glob import glob

#in_path = '/projects/topology_2010/output/images/ROIxTR_binary_persistence_Rips/'
#in_path = '/projects/topology_2010/output/images/ROIxTR_persistence_Rips/'
in_path = '/projects/topology_2010/output/tables/'
in_path_end = '.pdf'
out_path1 = in_path + 'ctrl/'
out_path2 = in_path + 'adhd/'

file_set1 = ['sub17078', 'sub31671', 
'sub18638', 'sub33062', 'sub19579', 
'sub33581', 'sub20732', 'sub35262',
'sub01912', 'sub21212', 'sub37864',
'sub02503', 'sub26267', 'sub38088',
'sub04856', 'sub27123', 'sub41546',
'sub05208', 'sub28795', 'sub44395',
'sub07578', 'sub28808', 'sub44515',
'sub09539', 'sub29216', 'sub44979',
'sub10011', 'sub29353', 'sub45217',
'sub10582', 'sub29935', 'sub46856',
'sub13384', 'sub30247', 'sub47087',
'sub15213', 'sub30623', 'sub47633',
'sub16607', 'sub30860', 'sub48830']

file_set2 = ['sub15758', 'sub31554', 
'sub73035', 'sub17109', 'sub48803', 
'sub77203', 'sub20676', 'sub53461', 
'sub77903', 'sub03951', 'sub20691', 
'sub54828', 'sub84371', 'sub08595', 
'sub22349', 'sub56734', 'sub12486', 
'sub22608', 'sub59796', 'sub14299', 
'sub23844', 'sub63915']

if __name__ == '__main__':
  # Iterate over subjects
  for ifile, in_file in enumerate(glob(in_path + '*' + in_path_end)):
#    if ifile < 4:
      file_name = in_file.split('/')[-1]
      file_id = file_name.split('_')[0]
      print('File: ' + file_name)
    
      if file_id in file_set1:
        cmd = 'cp ' + in_file + ' ' + out_path1 + file_name
      elif file_id in file_set2:
        cmd = 'cp ' + in_file + ' ' + out_path2 + file_name
      else:
        cmd = ''
      print(cmd); os.system(cmd)
