#!/usr/bin/env python

import  pd
from    sys         import argv, exit

if len(argv) < 2:
    print "Usage: %s FILENAME [MULTIPLIER=1] [NOISE=0] [RADIUS=.15] [DIMENSIONS=XMIN,YMIN,XMAX,YMAX]" % argv[0]
    print "  MULTIPLIER -   multiply coordinates of each point by this quantity"
    print "  NOISE -        filter out points below this persistence"
    print "  RADIUS -       radius of a point in the persistence diagram"
    print "  DIMENSIONS -   dimensions of the persistence diagram"
    print 
    print "  Example: %s torus.dgm 1 0 .05 -1,-1,10,10" % argv[0]
    exit()

multiplier =    float(argv[2])                  if len(argv) > 2    else 1
noise =         float(argv[3])                  if len(argv) > 3    else 0
R =             float(argv[4])                  if len(argv) > 4    else .15
dimensions =    map(float, argv[5].split(','))  if len(argv) > 5    else None

noise_filter =   pd.noise_filter(noise)
amplify_filter = pd.amplify_filter(multiplier)

dgm = pd.PersistenceDiagram(argv[1], lambda x,y: noise_filter(x,y) and amplify_filter(x,y))
dgm.savePDF(argv[1] + '.', radius = R, dimensions = dimensions)
