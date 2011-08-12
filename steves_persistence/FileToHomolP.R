# FileToHomolP R program

# Import
library(MASS)
library(Matrix)

# Files
snail <- c("sub01912")   #, ...)
inputdir <- "/projects/homology/output/tablesNEW/"
outputdir <- "/projects/homology/steves_persistence/output/homolp"
outputfileappend <- "_PrdyHomolDM.RData"

# Parameters
MAXDIM <- 1  # 3 for unDefMode; 1 for whole brain
trighs <- 2  # 3, or larger for defmode
xmsk <- unDefMode  # NULL  # whole brain
omitFreq <- 0
skiphomology <- FALSE  # TRUE just to create complexes for euler code

# Comment
xtrcmmnt <- "; default mode"  # "; whole brain"
xcmnt <- paste("MAXDIM=", MAXDIM, ", trighs=", trighs, ", omitFreq=", omitFreq, xtrcmmnt)
vrbst <- 2  # 0 for absolutely no comments (if bbb==0)!
bbb <- 5    # 0 for no followup comments
ydate <- date()


# BEGIN

for( i in 1:length(snail) ) {

if( !any(search() == "package:Matrix") )  {
cat("Yo! 'Matrix' isn't attached!")
break
}

snL <- snail[i]

cat("\n\n       NOW WORKING ON SUBJECT", i, ", viz., ", snL, ".\n")

xdate <- date()

xile <- paste(snL, "_filtered.csv", sep = "") 

# NOTE: This time I'm using the complement of 'defaultMode' as a "mask"!

system.time(
homol <- FileToHomolP(file.name = xile, TSEliot = NULL, rnames.in.col.1 = TRUE, roi.num = .8, thresh = .8, mask = xmsk, noHomol = skiphomology, omit.freq = omitFreq, kindOfBig = 37, drictree = inputdir, maxDim=MAXDIM, withEuler = FALSE, tires = trighs, DontSweatTheSmallStuff1 = 0, DontSweatTheSmallStuff2 = 12, traceIt = MAXDIM, checkAcyc = FALSE, IHaveMyLimits = 45000, constant.comment = xcmnt, verbosity = vrbst, blahblahblah = bbb)
)

SI()

alarm()

cat("  Started", xdate, "finished", date(), ".\n") # ('cat' prints strings. 'print' prints objects.)

cat(" Check filtration condition.\n")

x <- homol$homology.output # 
# ("$" is a way of extracting pieces from a composite object, like a list.)

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

yile <- paste(snL, outputfileappend, sep = "")

save( homol, file = paste(outputdir, yile, sep = "") )

rm(homol) # ('rm' removes objects.)

}

cat("\n\n       Done with this bunch. Started", ydate, "and now it's ...", date(), ".\n")

rm(MAXDIM, trighs, omitFreq, xcmnt, xmsk) 
