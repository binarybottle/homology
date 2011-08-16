
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
  kindobig <- 37
  MAXDIM <- 1
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

#---------------------
# FileToHomolP.R files
#---------------------
inputdir <- paste(maindir, "input/tables/", sep = "")
outputdir <- paste(maindir, "output/", sep = "")
outputfileappendP <- paste("_Homology_", commentID, ".RData", sep = "")
commentP <- paste("MAXDIM=", MAXDIM, ", trighs=", trighs, ", omitFreq=", omitFreq, ", ", commentID)

#----------------------
# FileToHomolFP.R files
#----------------------
outputfileappendFP <- paste("_FourierHomology_", commentID, ".RData", sep="")
commentFP <- paste("Fourier domain; Persistence-ready;", date(), "MAXDIM=", MAXDIM, ", trighs=", trighs,
                   ", omitFreq=", omitFreq, ", ", commentID)

#-----------------------
# FTHPobjToEuler.R files
#-----------------------
outputfileappendE <- paste("_Euler_", commentID, ".RData", sep = "")

