"""A script that calls some bash scripts"""

import pandas as pd
import os
import subprocess
from Bio import SeqIO

from Bio import AlignIO, Phylo
from Bio.Align.Applications import MuscleCommandline
import subprocess
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
#-------------------Functions
def gather_proteins(pair_file, col_proteins, protein_1, protein_2, output_dir):
    """Use grep to make the relevant proteins given a list of co-loc. terminal proteins"""

    # input check
    assert os.path.isfile(col_proteins), "the specified .faa-file does not exist"
    
    # run bash script
    basedir = os.path.dirname(__file__) # nessesary to find the location of the bash script
    cmd = " ".join(["bash", os.path.join(basedir,"get_faas.sh"),
                    pair_file,
                    col_proteins,
                    protein_1,
                    protein_2,
                    output_dir])
    subprocess.run(cmd,
                   shell=True)



def cluster_proteins(protein_fasta, output_dir):
    """Use CD-HIT to cluster proteins"""

    # input check
    assert os.path.isfile(protein_fasta), "the specified .faa-file does not exist"

    # run bash script
    basedir = os.path.dirname(__file__) # nessesary to find the location of the bash script
    cmd = " ".join(["bash", os.path.join(basedir,"cluster_by_cdhit.sh"),
                    protein_fasta,
                    output_dir])
    subprocess.run(cmd,
                   shell=True)

def clstr_to_table(clstr_file, output_file):
    """Convert clstr-file to a tsv for importing to R"""
    with open(clstr_file, 'r') as f, open(output_file, 'w') as out:
        cluster_num = -1
        for line in f:
            line = line.strip()
            if line.startswith(">Cluster"):
                cluster_num += 1
            else:
                # extract accession (up to first whitespace or full header)
                parts = line.split('>')
                if len(parts) > 1:
                    acc = parts[1].split('...')[0]
                    out.write(f"{acc}\t{cluster_num}\n")

#---------------------- Do all the things
output_dir = "results"
if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

repair_systems = ["tap_tpg",
                  "tac_tpc",
                  "gtpA_gtpB"]

for system in repair_systems:
    table_file = f"data/{system}_pairs_all.tsv"

    #------------------------------------------------------
    # PREFILTER WITH BASH
    prot1 = system.split("_")[0]
    prot2 = system.split("_")[1]
    
    gather_proteins(pair_file = table_file,
                       col_proteins="NBC_collected_proteins.faa",
                       protein_1=prot1,
                       protein_2=prot2,
                       output_dir=output_dir
                       )
    for protein in [prot1,prot2]:
        prot_fasta = os.path.join(output_dir,f"{protein}.faa")
        cluster_out = os.path.join(output_dir,f"{protein}_cluster")

        cluster_proteins(protein_fasta=prot_fasta,
                         output_dir=cluster_out)

        clstr_path = f"{cluster_out}.clstr"
        table_out = os.path.join(output_dir,f"{protein}_70.tsv")

        clstr_to_table(clstr_path,table_out)

