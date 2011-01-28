#!/usr/bin/python
from dionysus import Simplex, Filtration, StaticPersistence, dim_data_cmp, closure

t0 = [[64],[26,35],[54],[69],[2]]
t1 = [[64],[16,35,82],[26,35],[54],[69],[2]]
t2 = [[64],[16,35,82],[26,35],[54],[69],[33,81],[2]]
t3 = [[64],[16,35,82],[26,35],[54],[69],[8,71],[33,81],[2]]
times = [t0,t1,t2,t3]

kskeleton = 3

levels = []
for i, d in enumerate(times):
  for t in d:
    levels.append(Simplex(t, i))

levels.sort(key = lambda s: s.data)     # Sort the list by data

complex = closure(levels, kskeleton+1)

f = Filtration(complex, dim_data_cmp)
print "Complex in the filtration order:", ', '.join((str(s) for s in f))

p = StaticPersistence(f)
print "Persistence initialized"
p.pair_simplices()
print "Simplices paired"

smap = p.make_simplex_map(f)
for i in p:
    print i.sign(), i.pair().sign()
    print "%s (%d) - %s (%d)" % (smap[i], i.sign(), smap[i.pair()], i.pair().sign())
    print "Cycle (%d):" % len(i.cycle), " + ".join((str(smap[ii]) for ii in i.cycle))

print "Number of unpaired simplices:", len([i for i in p if i.unpaired()])
