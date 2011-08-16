
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
maindir <- "/Users/arno/Documents/homology/steves_persistence/"
inputdatafile <- paste(maindir, "Homology.RData", sep = "")
attach(inputdatafile)

#----------------------------------------------
# FileToHomolP.R and FileToHomolFP.R parameters
#----------------------------------------------
# Regions
useAllRegions <- 0  # 1 for all regions, 0 for subset (default mode regions)
if (useAllRegions == 1) {
  useMask <- NULL
  MAXDIM <- 1
  commentID <- "wholeBrain"
} else {
  useMask <- unDefMode
  MAXDIM <- 3
  commentID <- "defaultMode"
}
trighs <- 3
kindobig <- 37
ihavelimits <- 45000
donotsweat1 <- 0
donotsweat2 <- 12
threshRegions <- 0.8
threshActivity <- 0.8
omitFreq <- 0
vrbst <- 2  # 0 for absolutely no comments (if bbb==0)!
bbb <- 5    # 0 for no followup comments

#---------------------
# FileToHomolP.R files
#---------------------
inputdirP <- paste(maindir, "input/tables/", sep = "")
outputdirP <- paste(maindir, "output/homolp/", sep = "")
outputfileappendP <- paste("_PrdyHomol", commentID, ".RData", sep = "")
commentP <- paste("MAXDIM=", MAXDIM, ", trighs=", trighs, ", omitFreq=", omitFreq, ", ", commentID)

#----------------------
# FileToHomolFP.R files
#----------------------
inputdirFP <- paste(maindir, "output/homolp", sep = "")
outputdirFP <- paste(maindir, "output/homolfp", sep = "")
inputfileappendFP <- paste("_PrdyHomol", commentID, ".RData", sep = "")
commentFP <- paste("Fourier domain; Persistence-ready;", date(), "MAXDIM=", MAXDIM, ", trighs=", trighs,
                   ", omitFreq=", omitFreq, ", ", commentID)
# xthresh is tricky. In the Fourier domain, for the homological analysis angular frequencies
# take the place of time points. In the data I'm using the low pass filter is so aggressive
# that there are a lot of angular frequencies, about half, as I recall, at which there is
# virtually no power. So I thought that since only half of the angular frequencies have a
# chance to be "active", I should take as the "active" angular frequencies, instead of the
# top 20%, half of that, viz. 10%. That means I want a 90th, not 80th percentile threshold.
xthresh <- .9
outputfileappendFP <- paste("_FourierHomol", 10*xthresh, ".RData", sep="")

#-----------------------
# FTHPobjToEuler.R files
#-----------------------
inputdirE <- paste(maindir, "output/homolp/", sep = "")
outputdirE <- paste(maindir, "output/euler/", sep = "")
inputfileappendE <- paste("_PrdyHomol", commentID, ".RData", sep = "")
outputfileappendE <- paste("_Euler", commentID, ".RData", sep = "")

