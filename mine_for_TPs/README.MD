# Mine the G1034 collection for telomere maintanance machinery
Before starting a folder containing the genbank-files of all the complete genomes listed in data/complete.linear.G1034.txt
must be generated at results/G1034_complete_genomes. 


Script 01_genbank_to_faa.py can then be used to extract all proteins into a collected .faa-file.
Script 02_blast_run.sh can then be used to search the protein-file using data/terminal_proteins.faa as query
Script 03_terminal_protein_info.py can then be executed to extract extra information from the blast_results and genbank files used for plotting.

