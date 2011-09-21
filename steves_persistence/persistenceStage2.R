# Stage 2 persistencs R program

source("parameters.R")

args <- commandArgs(trailingOnly = TRUE)
subject <- args[1]

cat("\n  Working on subject", subject, ".\n")
startdate <- date()

inputfile <- paste(outputdir, subject, commentHomology, commentID, ".RData", sep="")

homolo <- homol$homology.output

# 'genealogy' is the main program for computing persistent homology from  "stage 1" output
persistentoutput <- genealogy(homol.list = homolo, ms=1, off.set = stage2tolevel1, damn = stage2dim, verbosity = 0)

detach(2)

# Save output
outputfile <- paste(subject, commentHomology, commentID, "_persistence.RData", sep="")
save( persistentoutput, file = paste(outputdir, outputfile, sep = "") )

rm(stage2dim, stage2tolevel1)
cat("\n\n       Done with subject ", subject, " -- started", startdate, "and ended", date(), "\n")
