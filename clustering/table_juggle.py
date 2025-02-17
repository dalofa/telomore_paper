import pandas as pd

uc_file = pd.read_csv("simplified_uc_file.tsv", 
                      sep="\t",
                      names=["seq_name",
                             "cluster_num",
                             "type"])
# remove double labeling with C and S (they are redundant)
uc_file_only_centroid = uc_file.loc[uc_file["type"]!="C"]
# get members of each cluster         
clust_mems = uc_file_only_centroid["cluster_num"].value_counts()
clust_mems.to_csv("clust_mems.tsv",
                  sep="\t")

# Make look_up_table for phylo look up
uc_file_only_centroid["seq_name"] = uc_file_only_centroid["seq_name"].str.replace("_left","")
uc_file_only_centroid["seq_name"] = uc_file_only_centroid["seq_name"].str.replace("_right_rc","")
look_up_tab = uc_file_only_centroid[["seq_name",
                                     "cluster_num"]]
look_up_tab.to_csv("look_up_table.tsv",
                   sep="\t",
                   index=False)