#!/bin/bash
###################
# BLAST-search for telomere maintanance machinery

# Check for the BLAST DB
if [ ! -f results/BLAST_comp_genome/all_proteins/NBC_collected_proteins.faa.db ]; then
    makeblastdb -dbtype prot -in results/BLAST_comp_genome/all_proteins/NBC_collected_proteins.faa -out results/BLAST_comp_genome/all_proteins/NBC_collected_proteins.faa.db 
fi

# Identify terminal proteins in NBC proteins from complete genomes
blastp -query data/terminal_proteins.faa -db results/BLAST_comp_genome/all_proteins/NBC_collected_proteins.faa.db -out results/BLAST_comp_genome/terminal_proteins_in_G1034.blast.txt -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qcovs" -max_target_seqs 100000 -evalue 1e-5  -num_threads 4
