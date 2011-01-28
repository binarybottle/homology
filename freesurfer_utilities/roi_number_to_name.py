"""
Convert ROI number to its name from a 2-column file
"""
import sys

#roi_number = sys.argv[1]
file_in = '/Applications/freesurfer/FreeSurferColorLUT.txt'

def roi_number_to_name(roi_number):
  f = open(file_in,'r')
  lines = f.readlines()
  for line in lines:
    if line != '':
      linesplit = line.split()
      if len(linesplit) > 0:
        if linesplit[0] == roi_number:
          return str(linesplit[1])
          break

#roi_name = roi_number_to_name(roi_number)
#print(roi_name)
