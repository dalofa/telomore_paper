#!/bin/bash
# Get logs

# Illumina logs
for folder in /bigdata/tuspjo/telomore_tester/streptomyces/take2/NBC*; do
	BASE=$(basename "$folder")
	echo $BASE
	for file in $folder/$BASE.topo_telomore_ill_telomore/*.log; do
		echo $(basename $file | cut -f1 -d"_")
		cat $file
	done


done
