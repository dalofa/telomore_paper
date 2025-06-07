#!/bin/bash
#----------------
# Script to grep all proteins the proteins, as this decreases run-time for the python script
#----------------

# Take inputs
input_file=$1
col_proteins=$2 # The fasta file of all NBC proteins
protein_1=$3
protein_2=$4
output_dir=$5

# Prep protein file
base_prot=$(basename "$col_proteins" | cut -d. -f1)
seqkit seq $col_proteins -w 0 > $base_prot.nowrap.faa

# get protein lists
cat $input_file | cut -f6 > $protein_1.txt
cat $input_file | cut -f7 > $protein_2.txt

# get and collect proteins
grep -f $protein_1.txt -F $base_prot.nowrap.faa -A1 --no-group-separator > $output_dir/$protein_1.faa
grep -f $protein_2.txt -F $base_prot.nowrap.faa -A1 --no-group-separator > $output_dir/$protein_2.faa

# Clean up some files
rm $protein_1.txt
rm $protein_2.txt
