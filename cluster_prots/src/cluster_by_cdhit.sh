#!/bin/bash

# Adjust input file and output folder
INPUT=$1
OUT_FILE=$2
# Run CD-HIT clustering at 0.70 identity (used to be at multiple identity thresholds)
cd-hit -i $INPUT -o $OUT_FILE -c 0.70 -n 4 -d 0
