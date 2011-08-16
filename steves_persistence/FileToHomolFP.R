# FileToHomolFP R program

args <- commandArgs(trailingOnly = TRUE)
subject <- args[1]

source("parameters.R")

#xdsss <- 12
snL <- subject

cat("\n  Working on subject", subject, ".\n")
startdate <- date()

inputfile <- paste(subject, commentHomology, commentID, ".RData", sep="")

# Takes an 'FileToHomolP' output file as input.

commentLocal <- paste("Fourier domain; Persistence-ready;", date(), "MAXDIM=", MAXDIM, ", trighs=", trighs,
                   ", omitFreq=", omitFreq, ", ", commentID)

system.time( homol <- FileToHomolFP(file.name = inputfile, TSEliot = NULL, rnames.in.col.1 = FALSE,
                                    roi.num = threshRegions, thresh = threshActivity, mask = useMask, noHomol = FALSE,
                                    omit.freq = omitFreq, kindOfBig = kindobig, maxDim=MAXDIM, drictree = outputdir,
                                    aList = NULL, withEuler = FALSE, tires = trighs,
                                    DontSweatTheSmallStuff1 = donotsweat1, DontSweatTheSmallStuff2 = donotsweat2,
                                    traceIt = MAXDIM, returnReducedMat = TRUE, checkAcyc = FALSE,
                                    IHaveMyLimits = ihavelimits, constant.comment = commentLocal,
                                    verbosity = vrbst, blahblahblah = 3) )

SI()

cat(" Check filtration condition.\n")

x <- homol$homology.output

n <- length(x) 

if(n > 1) {
    zyx <- matrix(rep(NA, 2*(n-1)), ncol = 2)
    dimnames(zyx) <- list( as.character(2:n), c("acyclic", "wholeEnchilada") )

    for(i in 2:n) {
        xaw <- x[[i]]$excisionTrickPOutput; xaw <- xaw$AandWs
        xa <- xaw$acyclic
        xxx <- append(xa, xaw$whatsLeft)

        yaw <- x[[i-1]]$excisionTrickPOutput; yaw <- yaw$AandWs
        ya <- yaw$acyclic
        yyy <- append(ya, yaw$whatsLeft)

        zyx[i-1, "acyclic"] <- subCmplx(xa, ya)
        zyx[i-1, "wholeEnchilada"] <- subCmplx(xxx, yyy)
    }

    if( all( apply(zyx, 2, all) ) ) {
        cat("   Just as filtered as filtered can be!\n")
    } else {
        cat("\n   SUBJECT", subject, "IS NOT FILTERED! HERE'S SAD STORY:\n")
        print(zyx)
        break
    }
} else {
  cat("  Only one frequency level.  'Filteredness' isn't an issue.\n")
}

# Save output

outputfile <- paste(subject, commentFourierHomology, commentID, ".RData", sep="")
save( homol, file = paste(outputdir, outputfile, sep = "/") )
rm(homol, MAXDIM, trighs, omitFreq, commentFourierHomology, useMask)

cat("\n\n       Done with subject ", subject, " -- started", startdate, "and ended", date(), "\n")
# This celebratory signal indicates when a subject is finished. If you've got 40 processors going,
# the din might drive you crazy so you might want to comment this out.
# alarm()

