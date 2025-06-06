"""A script for generating a collected fasta file of all proteins from NBC collection"""
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import os
import glob
import sys


def genbank_to_fasta(genbank_file, fasta_file, strain_name):
    
    # Read the GenBank file
    records = SeqIO.parse(genbank_file, "genbank")
    
    # List to store the protein SeqRecords
    protein_records = []

    for record in records:
        for feature in record.features:
            # Check if the feature is a CDS (Coding Sequence)
            if feature.type == "CDS":
                # Extract the protein sequence from the CDS feature
                if 'translation' in feature.qualifiers:
                    protein_seq = feature.qualifiers['translation'][0]
                    # Create an identifier for the protein
                    accession = record.annotations['accessions'][0]
                    protein_id = feature.qualifiers.get('protein_id', ['unknown_protein'])[0]
                    header = f"{strain_name}_{accession}_{protein_id}"
                    # Create a SeqRecord for the protein sequence
                    protein_record = SeqRecord(Seq(protein_seq),
                                               id=header,
                                               description=feature.qualifiers.get('product', [''])[0])
                    # Add the protein SeqRecord to the list
                    protein_records.append(protein_record)
    
    # Write the protein sequences to a FASTA file
    SeqIO.write(protein_records, fasta_file, "fasta")

# Make the output folder if it does not exits
folder_path = "results/BLAST_comp_genome/all_proteins"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)


# go through all complete genomes:
for genbank in glob.glob("results/G1034_complete_genomes/*gb"):
    strain_name = genbank.split("/")[-1][0:9]
    output_path = os.path.join("results/BLAST_comp_genome/all_proteins",strain_name+".faa")
    genbank_to_fasta(genbank,output_path,strain_name)
    print("Finished",strain_name)

# Concat the files into a single file
output_file = "results/BLAST_comp_genome/all_proteins/NBC_collected_proteins.faa"

# Open the output file in write mode
with open(output_file, 'w') as outfile:
    # Iterate over all .faa files in the current directory
    for faa_file in glob.glob("results/BLAST_comp_genome/all_proteins/*.faa"):
        if "NBC_collected_proteins" in faa_file:
            continue
        elif "NBC_tpg_blast_proteins" in faa_file:
            continue
	# Open each .faa file in read mode
        with open(faa_file, 'r') as infile:
            # Write the contents of the .faa file into the output file
            outfile.write(infile.read())
        os.remove(faa_file)

print(f"All .faa files have been concatenated into {output_file}")


