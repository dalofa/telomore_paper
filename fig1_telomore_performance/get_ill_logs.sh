#!/bin/bash
# Get logs

# Illumina logs
# Streptos
for folder in /bigdata/tuspjo/telomore_tester/streptomyces/take2/NBC*; do
	
	if [[ -d $folder ]]; then
		BASE=$(basename "$folder")
		echo $BASE
		for file in $folder/$BASE.topo_telomore_ill_telomore/*.log; do
			echo $(basename $file | cut -f1 -d"_")
			cat $file
		done
	fi
done
# Kitosatospora
for folder in /bigdata/tuspjo/telomore_tester/kitasatospora/100_strain_folders/NBC*; do
	
	if [[ -d $folder ]]; then
		BASE=$(basename "$folder")
		echo $BASE
		for file in $folder/$BASE.topo_telomore_ill_telomore/*.log; do
			echo $(basename $file | cut -f1 -d"_")
			cat $file
		done
	fi

done
# Embleya
for folder in /bigdata/tuspjo/telomore_tester/embleya/NBC*; do

	if [[ -d $folder ]]; then
		BASE=$(basename "$folder")
		echo $BASE
		for file in $folder/$BASE.topo_telomore_ill_telomore/*.log; do
			echo $(basename $file | cut -f1 -d"_")
			cat $file
		done
	fi

done
