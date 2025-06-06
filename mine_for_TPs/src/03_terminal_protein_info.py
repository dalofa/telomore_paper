"""A script for parsing collected BLAST-file of terminal protein into tables for plotting"""

from Bio import SeqIO
import pandas as pd
import glob

# Dict of accessions to protein name
acc_to_name = {"CAC22742.1":"Tpg",
                "CAC22741.1":"Tap",
                "CAC36648.1":"Tpc",
                "CAC36646.1":"Tac",
                "BAG16926.1":"GtpA",
                "BAG16927.1":"GtpB"}

fmt_6_headers=["qseqid", "sseqid", "pident",
               "length", "mismatch", "gapopen",
               "qstart", "qend", "sstart",
               "send", "evalue", "bitscore","qcovs"]

BLAST_results=pd.read_csv("results/BLAST_comp_genome/terminal_proteins_in_G1034.blast.txt",
    sep="\t",
    names=fmt_6_headers)

# Rename BLAST results to protein function
for acc in acc_to_name:
    BLAST_results = BLAST_results.replace(acc,acc_to_name[acc])

protein_matches = []
# Grab information from genbank file 
for result in BLAST_results.iterrows():
    # information to retrieve hit
    match_id = result[1].sseqid
    protein_match=result[1].qseqid
    strain_name = "_".join(match_id.split("_")[0:2]) # needed as _ occurs in NBC_xxxxx
    #acession = match_id.split("_")[2] this be wrong
    protein_id = "_".join(match_id.split("_")[3:5])

    # information about hit quality
    pident = result[1].pident
    evalue = result[1].evalue
    qcovs = result[1].qcovs
    
    # Pull hit out of genbank file
    genbank_path = "results/G1034_complete_genomes/" +strain_name +"*"

    for file in glob.glob(genbank_path):
    
        if strain_name in file:
            print("checking",file)
            for record in SeqIO.parse(file,"genbank"):
                topology = record.annotations.get('topology')
                for feat in record.features:
                    if feat.type=="source":
                        source_info = feat.qualifiers
                        taxon = source_info["organism"]
                        
                    if feat.type=="CDS" and "protein_id" in feat.qualifiers:
                        #print(feat.qualifiers["protein_id"])
                        #print([protein_id])
                        if [protein_id]==feat.qualifiers["protein_id"]:
                            location = feat.location
                            product= feat.qualifiers["product"]
                            length = len(record)
                            acession = record.id

                            if "plasmid" in source_info:
                                DNA="plasmid"
                            elif "extrachromosomal" in str(source_info):
                                DNA="extrachromosomal"
                            else:
                                DNA="chromosome"



                            protein_matches.append([protein_match,strain_name,acession,taxon,DNA,topology,length,protein_id,location,product,pident,evalue,qcovs])

# Transform list of results into dataframe and print to file
protein_matches_df = pd.DataFrame(protein_matches,columns=["protein_match", "strain_name","accession","taxon","DNA_type","DNA_topolgy","DNA_length","protein_id","location","product","pident","evalue","qcov"])

# write collected dataframe to file
protein_matches_df.to_csv("results/BLAST_comp_genome/term_prot_BLAST_info.tsv",sep="\t")
