(8/12/'11)

Description of Steve's computational homology package. (DRAFT)

My key functions use the R library "Matrix". One functin ues the "MASS" libray. You get them by entering

library(Matrix)
library(MASS)

Note that to print out an R object, you just paste or type in the name of the object and hit enter.  E.g., tyr

StevesPersistntHomol <rtrn>

defaultMode: A list of region codes for the 41 regions in the "default mode network". (Do those codes have the same meaning in different sites?) 

unDefMode: Codes for the 52 regions NOT in the "default mode network".

SI: Short hand for "save.image". It saves the work space to an ".RData" file.

StevesPersistntHomol:  Main program. It computes homology.

FileToHomolP: Reads in BOLD data, constructs corresponding complex, filters the complex by frequency level, calls 'StevesPersistntHomol' for every frequency level (in such a way that persistence can be derived later), and packages results.




EXAMPLE OF USE OF 'FileToHomolP': 


MAXDIM <- 2

trighs <- 3

omitFreq <- 1

bbb <- 5

xmsk <- unDefMode

xcmnt <- paste("MAXDIM=", MAXDIM, ", trighs=", trighs, ", omitFreq=", omitFreq, "; default mode")

# Code starts here.

ydate <- date()

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
homol <- FileToHomolP(file.name = xile, TSEliot = NULL, rnames.in.col.1 = TRUE, roi.num = .8, thresh = .8, mask = xmsk, noHomol = FALSE, omit.freq = omitFreq, kindOfBig = 37, drictree = "/data/Research/ComputationalHomol/Topology_of_Brain_Associations/ADHD_data2/tables_5_9_11", maxDim=MAXDIM, withEuler = FALSE, tires = trighs, DontSweatTheSmallStuff1 = 0, DontSweatTheSmallStuff2 = 12, traceIt = 2, checkAcyc = FALSE, IHaveMyLimits = 45000, constant.comment = xcmnt, verbosity = 2, blahblahblah = bbb)
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

yile <- paste(snL, "_PrdyHomolDM.RData", sep = "")

save( homol, file = paste("/data/Research/ComputationalHomol/Topology_of_Brain_Associations/ADHD_data2/homology_files/Spring11_dir/TimeDomain_dir/Persistence/StevesPersistentHomolOutput/DefaultMode/", yile, sep = "") )

rm(homol) # ('rm' removes objects.)

}

cat("\n\n       Done with this bunch. Started", ydate, "and now it's ...", date(), ".\n")

rm(MAXDIM, trighs, omitFreq, xcmnt, xmsk) 

END OF EXAMPLE.






extractBettis: Extracts Betti numbers from objects like that produced by 'FileToHomolP'.

dtrend:  Removes linear trend (both in level and in spread) from a time series.  Requires "library(MASS)".  Oddly, I haven't been using 'dtrend'!

graduate: Filters a complex by frequency level.

KleinBottle:  A complex that can be used for testing 'StevesPersistntHomol'.

Torus: Another complex that can be used for testing 'StevesPersistntHomol'.


EXAMPLE:

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

END OF EXAMPLE.




acyclic: Checks to see if a complex is "acyclic" (no homology; hole free). If it returns TRUE then the complex is acyclic. If it returns FALSE, that just means that it failed to demonstrate that the complex is acyclic. 

addColumns2: Takes two columns of a "sparseMatrix" with 0-1 entries and adds them mod 2. (Essentially, it performs element-wise exclusive OR).

aggrandizeP: Greedily tries to assemble a big acyclic subset of a complex.

Betty0: Computes 0-dimensional Betti number of a complex.

deredundate: Removes redundant simplices from a complex.

blunt: Simplifies a complex by removing protruding vertices.

blunt.one: Used by 'blunt'.

boil.down: uses 'blunt' and 'deredundate' to simplify a complex.

boildown.filtered.cmplx: Simplifies "frames" in a filtered complex in such a way that the output is still filtered. (Important for computing persistence.)

BOLD.to.Complex: Takes a floating point matrix of BOLD values and computes a "Curto-Itskov" complex of the active time points.

eulerNumber: Computes the Euler number of a complex. (This function should probaly be called 'eulerCharacteristic'.)

FTHP.obj.ToEuler: Takes an object like that spewed forth by 'FileToHomolP' and a number or character string specifying a frequency level and returns the Euler characteristic of the complex at that frequency level.




# EXAMPLE OF USE OF 'FTHP.obj.ToEuler'.

# Compute Euler numbers in frequency levels 

x <- 1:4 # (i.e., 1 through 4.)

# For subjects

snail <- c("sub18638", "sub26267", "sub54828")

# Make a matrix to hold output.

HoustonEulers <- matrix( rep(NA, length(snail) * length(x)), ncol = length(x) )

# Give helpful names to the rows and columns.

dimnames( HoustonEulers ) <- list( snail, as.character(x) )

# For purposes of reading in files:

xdn <- "/data/Research/ComputationalHomol/Topology_of_Brain_Associations/ADHD_data2/homology_files/Spring11_dir/TimeDomain_dir/Persistence/StevesPersistentHomolOutput/DefaultMode/"

xuf <- "_PrdyHomolDM.RData"

yile <- paste(snL, xuf, sep = "")


for(snL in snail) {

# Print out reassurance.

cat("\n  Working on subject", snL, ".\n")

# Read in an 'FileToHomolP' output file.

yile <- paste(snL, xuf, sep = "")

attach( paste(xdn, yile, sep = "") )

# Compute the Euler characteristics for all the frequency levels in 'x' "at once". Assume that the homology in the file is packaged in something called 'homol'.

HoustonEulers[ snL, ] <- sapply( x, FTHP.obj.ToEuler, FTHP.obj = homol )

# Release the file.

detach(2)

}


# Behold:

HoustonEulers
         1  2 3 4
sub18638 0 10 6 0
sub26267 4 -3 7 1
sub54828 1  1 1 1

END OF EXAMPLE.




excisionTrickP: Uses 'aggrandizeP' to divide a complex into a acylic subcomplex and all the rest. Then it "excises" most of the acyclic part away.

familyResemblance: Given a simplex and a complex, it looks for simplices in the complex that resemble the given simplex in some fashion that you can choose from a short list.

grepGrab: Obscure function that's used in comparing Betti numbers with what Sage gets.

intersectionOfComplexes: Just what the name implies.

listListToListVec: Converts one representation of a complex into the standard one. 

listUnion: Given a list of vectors, returns the set theoretic union of all the vectors in the list. E.g., given a complex it returns a vector of all the simplices in the complex, each listed just once.

querulous: Computes the interquartile range of a vector of numbers. Same as built in function 'IQR'.

reduceLeftToRight: An important function that simplifies 0-1 matrices mod 2.

SubSet: Determines whether the first argument is a subset of the second.

SetSub: Determines whether the second argument is a subset of the first.

simpCmpx.print: Obscure function that's used in comparing Betti numbers with what Sage gets.

simpFinder: Finds all simplices in a complex of a given dimension.

simpListIntersect: Finds all vertices that belong to all the simplices in a complex.

subCmplx: Determines whether one complex is a subcomplex of another.

symmDiff: Computes the symmetric difference of two vectors.

thresholdSimplices: Identifies consensuses (consensi?) that appear at least a given number of times in a list of consensi.

FileToHomolFP: Orchestrates homology analysis in Fourier domain.



# EXAMPLE OF USE OF 'FileToHomolFP':

# This it tricky. In the Fourier domain, for the homological analysis angular frequencies take the place of time points. In the data I'm using the low pass filter is so aggressive that there are a lot of angular frequencies, about half, as I recall, at which there is virtually no power. So I thought that since only half of the angular frequenies have a chance to be "active", I should take as the "active" angular frequencies, instead of the top 20%, half of that, viz. 10%.  That means I want a 90th, not 80th percentile threshold.

xthresh <- .9

outDir <- "/data/Research/ComputationalHomol/Topology_of_Brain_Associations/ADHD_data2/homology_files/Spring11_dir/AngularFrequencyDomain_dir/AngularFrequencyDomain.9_dir/Persistence/"

MAXDIM <- 2
xdsss <- 12

ydate <- date()

for( i in 1:length(snail) ) { # As usual 'snail' is a vector of subject names.

if( !any(search() == "package:Matrix") )  {
cat("\n\n   Yo! 'Matrix' isn't attached!\n\n")
break
}

snL <- snail[i]

cat("\n\n       NOW WORKING ON SUBJECT", i, ", viz., ", snL, ".\n")

xdate <- date()

yile <- paste(snL, "_PrdyHomol.RData", sep = "")

# Takes an 'FileToHomolP' output file as input.

system.time( homol <- FileToHomolFP(file.name = yile, TSEliot = NULL, rnames.in.col.1 = FALSE, roi.num = .8, thresh = xthresh, mask = NULL, noHomol = FALSE, omit.freq = 1, kindOfBig = 37, maxDim=MAXDIM, drictree ="/data/Research/ComputationalHomol/Topology_of_Brain_Associations/ADHD_data2/homology_files/Spring11_dir/TimeDomain_dir/Persistence/StevesPersistentHomolOutput", aList = NULL, withEuler = FALSE, tires = 3, DontSweatTheSmallStuff1 = 0, DontSweatTheSmallStuff2 = 12, traceIt = 2, returnReducedMat = TRUE, checkAcyc = FALSE, IHaveMyLimits = 45000, constant.comment = paste("Fourier domain; Persistence-ready;", date()), verbosity = 1, blahblahblah = 3) )

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

cat("  Started", xdate, "finished", date(), ".\n")

# Use a special name to indicate that you're doin' Fourier.

zile <- paste(snL, "_Prdy_FourierHomol", 10*xthresh, "RData", sep = ".") 

save( homol, file = paste(outDir, zile, sep = "/") )

rm(homol)

}

cat("\n\n       Done with this bunch. Started", ydate, "and now it's ...", date(), ".\n")

# END OF EXAMPLE.



