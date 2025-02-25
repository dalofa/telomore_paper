#!/bin/bash
# Get logs

# Nanopore logs
for folder in /bigdata/tuspjo/telomore_tester/streptomyces/take2/NBC*; do
	BASE=$(basename "$folder")
	echo $BASE
	for file in $folder/$BASE.topo_np_telomore/*.log; do
		echo $(basename $file | cut -f1 -d"_")
		cat $file
	done


done


# Kitosatospora
for folder in /bigdata/tuspjo/telomore_tester/kitasatospora/100_strain_folders/NBC*; do
	
	if [[ -d $folder ]]; then
		BASE=$(basename "$folder")
		echo $BASE
		for file in $folder/$BASE.topo_np_telomore/*.log; do
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
			for file in $folder/$BASE.topo_np_telomore/*.log; do
				echo $(basename $file | cut -f1 -d"_")
				cat $file
			done
	fi

done