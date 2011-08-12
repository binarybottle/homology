# Compute Euler numbers in frequency levels 

x <- 2:4 # (i.e., 2 through 4.)

outputdir <- "/drop/share_homology/Steves_homology_code/output/euler/"
inputfileappend <- "_PrdyHomolDM.RData"  # "_PrdyHomol.RData"
outputfileappend <- "_Euler.RData"  # "_EulerDM.RData"

ydate <- date()

# For subjects

inputdir <- "/drop/share_homology/Steves_homology_code/output/homolp/"  # /homolfp/"
snail <- c("sub01912")  #(sub18638", "sub26267", "sub54828")

# Make a matrix to hold output.

HoustonEulers <- matrix( rep(NA, length(snail) * length(x)), ncol = length(x) )

# Give helpful names to the rows and columns.

dimnames( HoustonEulers ) <- list( snail, as.character(x) )

# For purposes of reading in files:

xdn <- inputdir

yile <- paste(snL, inputfileappend, sep = "")


for(snL in snail) {

# Print out reassurance.

cat("\n  Working on subject", snL, ".\n")

# Read in an 'FileToHomolP' output file.

yile <- paste(snL, inputfileappend, sep = "")

attach( paste(xdn, yile, sep = "") )

# Compute the Euler characteristics for all the frequency levels in 'x' "at once". Assume that the homology in the file is packaged in something called 'homol'.

HoustonEulers[ snL, ] <- sapply( x, FTHP.obj.ToEuler, FTHP.obj = homol )

# Release the file.

detach(2)

zile <- paste(snL, outputfileappend, sep = "")
save( HoustonEulers, file = paste(outputdir, zile, sep = "") )
rm(HoustonEulers) # ('rm' removes objects.)

}

cat("\n\n       Done with this bunch. Started", ydate, "and now it's ...", date(), ".\n")

