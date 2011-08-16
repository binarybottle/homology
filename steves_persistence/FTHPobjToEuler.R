# Compute Euler numbers in frequency levels 

args <- commandArgs(trailingOnly = TRUE)
subject <- args[1]

source("parameters.R")

cat("\n  Working on subject", subject, ".\n")
startdate <- date()

x <- 2:4 # (i.e., 2 through 4.)

# Make a matrix to hold output.
#HoustonEulers <- matrix( rep(NA, length(subjects) * length(x)), ncol = length(x) )
# Give helpful names to the rows and columns.
#dimnames( HoustonEulers ) <- list( subjects, as.character(x) )

# Read in file.
inputfile <- paste(subject, outputfileappendP, sep = "")
attach( paste(outputdir, inputfile, sep = "") )

# Compute the Euler characteristics for all the frequency levels in 'x' "at once".
# Assume that the homology in the file is packaged in something called 'homol'.
#HoustonEulers[ subject, ] <- sapply( x, FTHP.obj.ToEuler, FTHP.obj = homol )
# Release the file.
#detach(2)
HoustonEulers <- sapply( x, FTHP.obj.ToEuler, FTHP.obj = homol )

# Save output
outputfile <- paste(subject, outputfileappendE, sep = "")
save( HoustonEulers, file = paste(outputdir, outputfile, sep = "") )
rm(HoustonEulers)

cat("\n\n       Done with subject ", subject, " -- started", startdate, "and ended", date(), "\n")
# This celebratory signal indicates when a subject is finished. If you've got 40 processors going,
# the din might drive you crazy so you might want to comment this out.
# alarm()

