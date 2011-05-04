#!/usr/bin/python
"""
R code for robust detrending of data.
Requires "MASS": library(MASS)

(c) Steve Ellis (R code; revised 4/2011)

Arno Klein  .  arno@binarybottle.com  .  2011  .  MIT license
"""

import rpy2.robjects as robj

robj.r('library(MASS)')

#data = [0,1,2,2,2,2,2,2,3,4]
#robj.r.assign('y', data)

rdetrend = robj.r("""
detrend <- function(y, preserve.stats = TRUE, I.want.it.all = FALSE, verbose = FALSE, upset = .1) {

x <- 1:length(y)
# Keep track of where the NA's are.
z <- is.na(y)
yy <- y[!z]
xx <- x[!z]

# If there's no spread in the data then detrending isn't needed.
quyy <- IQR(yy)
myy <- abs(median(yy))
if( myy < 0.000001) myy <- 1
if(quyy/myy  < 0.000001) {
    cat("  No spread in data. No need to detrend.\n")
    return(y)
}

treg <- rlm(yy ~ xx)
yr <- treg$residuals

quyr <- IQR(yr) # ('IQR' computes the interquartile range.)

sreg <- NULL

if(quyr < 0.00001) { syr <- 1 } else {
    ayr <- log(abs(yr/quyr) + upset)
    sreg <- rlm(ayr ~ xx)
    if(sreg$converged) { 
        syr <- exp(sreg$fitted.values)
    } else {
        cat("  'rlm' didn't converge.     dtrend -- \n")
        syr <- median(abs(yr))
    }
}

if(verbose) {
    cat("   'syr'                 -- dtrend\n")
    print(syr)
}

ys <- yr/syr

crrxn <- 1
qys <- IQR(ys)
if(preserve.stats) {
    if(qys < 0.00001) {
        cat("  NO SPREAD IN RESIDUALS. CAN'T PRESERVE STATISTICS!\n")
    } else { 
        crrxn <- quyy/qys 
    }
}

ys <- ys * crrxn

crrxn <- 0
if(preserve.stats) crrxn <- median(yy) - median(ys)
ys <- ys + crrxn

# Put NA's back.

newy <- rep(NA, length(z))
newy[xx] <- ys
if(I.want.it.all) {
    return(list(detrended.series = newy, location.reg = treg, scale.reg = sreg))
}
newy

}
""")