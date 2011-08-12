# FileToHomolFP R program

# Import
library(MASS)
library(Matrix)

# Files
snail <- c("sub01912")   #, ...)
outputdir <- "/drop/share_homology/Steves_homology_code/output/homolfp"
inputdir <- "/drop/share_homology/Steves_homology_code/output/homolp"  # /homolfp/"
inputfileappend <- "_PrdyHomolDM.RData"

# This it tricky. In the Fourier domain, for the homological analysis angular frequencies take the place of time points. In the data I'm using the low pass filter is so aggressive that there are a lot of angular frequencies, about half, as I recall, at which there is virtually no power. So I thought that since only half of the angular frequenies have a chance to be "active", I should take as the "active" angular frequencies, instead of the top 20%, half of that, viz. 10%.  That means I want a 90th, not 80th percentile threshold.
xthresh <- .9
outputfileappend <- paste("_FourierHomol", 10*xthresh, ".RData", sep="")

# Parameters
MAXDIM <- 1  # 3 for unDefMode; 1 for whole brain
trighs <- 2  # 3, or larger for defmode
xmsk <- unDefMode  # NULL  # whole brain
omitFreq <- 0
xdsss <- 12

# Comment
xtrcmmnt <- "; default mode"  # "; whole brain"
xcmnt <- paste("Fourier domain; Persistence-ready;", date(), "MAXDIM=", MAXDIM, ", trighs=", trighs, ", omitFreq=", omitFreq, xtrcmmnt)
vrbst <- 2  # 0 for absolutely no comments (if bbb==0)!
bbb <- 5    # 0 for no followup comments
ydate <- date()


# BEGIN

for( i in 1:length(snail) ) { # As usual 'snail' is a vector of subject names.

if( !any(search() == "package:Matrix") )  {
cat("\n\n   Yo! 'Matrix' isn't attached!\n\n")
break
}

snL <- snail[i]

cat("\n\n       NOW WORKING ON SUBJECT", i, ", viz., ", snL, ".\n")

yile <- paste(snL, inputfileappend, sep = "")

# Takes an 'FileToHomolP' output file as input.

system.time( homol <- FileToHomolFP(file.name = yile, TSEliot = NULL, rnames.in.col.1 = FALSE, roi.num = .8, thresh = xthresh, mask = xmsk, noHomol = FALSE, omit.freq = omitFreq, kindOfBig = 37, maxDim=MAXDIM, drictree = inputdir, aList = NULL, withEuler = FALSE, tires = 3, DontSweatTheSmallStuff1 = 0, DontSweatTheSmallStuff2 = 12, traceIt = MAXDIM, returnReducedMat = TRUE, checkAcyc = FALSE, IHaveMyLimits = 45000, constant.comment = xcmnt, verbosity = vrbst, blahblahblah = 3) )

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
cat("\n   SUBJECT", snL, "IS NOT FILTERED! HERE'S SAD STORY:\n")
print(zyx)
break
   }
          } else { 
cat("  Only one frequency level.  'Filteredness' isn't an issue.\n")
       }

alarm()  # This celebratory signal indicates when a subject is finished. If you've got 40 processors going, the din might drive you crazy so you might want to comment this out.

cat("  Started", ydate, "finished", date(), ".\n")

# Use a special name to indicate that you're doin' Fourier.

zile <- paste(snL, outputfileappend, sep = ".") 

save( homol, file = paste(outputdir, zile, sep = "/") )

rm(homol)

}

cat("\n\n       Done with this bunch. Started", ydate, "and now it's ...", date(), ".\n")

