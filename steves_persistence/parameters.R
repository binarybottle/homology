
# Import
library(MASS)
library(Matrix)

if( !any(search() == "package:Matrix") )  {
  cat("'Matrix' isn't attached!")
  break
}
if( !any(search() == "package:MASS") )  {
  cat("'MASS' isn't attached!")
  break
}

#-----------------------------------------
# FileToHomolP.R and FileToHomolFP.R files
#-----------------------------------------
maindir <- "/Users/arno/Documents/Projects/homology/steves_persistence/"
inputdir <- paste(maindir, "input/tables/", sep = "")
outputdir <- paste(maindir, "output/", sep = "")
inputdatafile <- paste(maindir, "Homology.RData", sep = "")
attach(inputdatafile)

#----------------------------------------------
# FileToHomolP.R and FileToHomolFP.R parameters
#----------------------------------------------
# Regions
useAllRegions <- 1  # 1 for all regions, 0 for subset (default mode regions)
if (useAllRegions == 1) {
  useMask <- NULL
  MAXDIM <- 3 # 1
  kindobig <- 22 # 37
  commentID <- "wholeBrain"
} else {
  useMask <- unDefMode
  MAXDIM <- 3
  kindobig <- 22
  commentID <- "defaultMode"
}
trighs <- 2
ihavelimits <- 45000
donotsweat1 <- 0
donotsweat2 <- 12
threshRegions <- 0.8
threshActivity <- 0.8
omitFreq <- 0
vrbst <- 2  # 0 for absolutely no comments (if bbb==0)!
bbb <- 5    # 0 for no followup comments

#--------------------------
# FileToHomolP.R and
# FileToHomolFP.R and
# FTHPobjToEuler.R comments
#--------------------------
commentHomology <- "_Homology_"
commentFourierHomology <- "_FourierHomology_"
commentEuler <- "_Euler_"

#--------
# Stage 2
#--------
stage2dim <- 1  # Dimension in which you want to compute persistence. Repeat for all dimensions, bigger than 0, for which you've done the "stage 1" calculations.
stage2tolevel1 <- 0  # Go all the way down to frequency level 1.
