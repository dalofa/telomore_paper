"""
Script to make a table of replicons name to replicon type for plotting figures.
"""


import pandas as pd
import glob
from Bio import SeqIO

info = []
genbank_path = "/home/WIN.DTU.DK/dalofa/telomore_paper/fig1_telomore_performance/all_genomes/*" 
for file in glob.glob(genbank_path):
    print(file)

    for record in SeqIO.parse(file,"genbank"):
        
        contig = record.id
        for feat in record.features:

            if feat.type=="source":
                source_info = feat.qualifiers
                taxon = source_info["organism"]
                strain = source_info["strain"]
                print(source_info)

                if "plasmid" in source_info:
                    DNA="plasmid"
                elif "extrachromosomal" in str(source_info):
                    DNA="extrachromosomal"
                else:
                    DNA="chromosome"
               
        info.append([contig,strain,taxon,DNA])
            

df = pd.DataFrame(info,columns=["contig_name",
                                "strain_name",
                                "taxon",
                                "rep_type"])

df.to_csv(path_or_buf="rep_type.tsv",
          sep="\t",
          index=False)