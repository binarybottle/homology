xsch <- StevesPersistntHomol(Torus, dimRange = c(0,3), reducer = reduceLeftToRight, verbosity = 2, traceIt = 2, returnReducedMat = TRUE, returnBoundaryMatrix = TRUE)

xsch$BettiNumbers

# Should return:

0 1 2 3 
1 2 1 0

xsch <- StevesPersistntHomol(KleinBottle, dimRange = c(0,3), reducer = reduceLeftToRight, verbosity = 2, traceIt = 2, returnReducedMat = TRUE, returnBoundaryMatrix = TRUE)

xsch$BettiNumbers

# Should return the same thing.

# While we're at it, try a "2-sphere":

sph <- list( c(1,2,3), c(2,3,4), c(1,3,4), c(1,2,4) )

xsch <- StevesPersistntHomol( sph , dimRange = c(0,3), reducer = reduceLeftToRight, verbosity = 2, traceIt = 2, returnReducedMat = TRUE, returnBoundaryMatrix = TRUE)

xsch$BettiNumbers

# Should return:

0 1 2 3 
1 0 1 0

# "3-sphere":

sph <- list( c(1,2,3,4), c(1,2,3,5), c(1,2,4,5), c(1,3,4,5),  c(2,3,4,5))

xsch <- StevesPersistntHomol( sph , dimRange = c(0,3), reducer = reduceLeftToRight, verbosity = 2, traceIt = 2, returnReducedMat = TRUE, returnBoundaryMatrix = TRUE)

xsch$BettiNumbers

# Should return:

0 1 2 3 
1 0 0 1

rm(xsch, sph)
