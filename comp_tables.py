"""
Script to combine extension table with clustering table in order to find a good example for figure 2 in the paper.
"""

import pandas as pd

ext_table = pd.read_csv(filepath_or_buffer= "fig1_telomore_performance/comb_NP_and_ill.tsv",
                        sep="\t")
clust_table = pd.read_csv(filepath_or_buffer= "clustering/simplified_uc_file.tsv",
                        sep="\t",
                        names= ["rep_end","clust_num","type"])

# add replicon column
clust_table["replicon"] = clust_table['rep_end'].str.split('_').str[0]


# merge the dataframes
merged_df = pd.merge(left = ext_table,
                     right = clust_table,
                     on="replicon",
                     how="inner")
# filter for group2 members
group_2 = merged_df[merged_df["clust_num"]==2]

group_2.to_csv(path_or_buf="clust2_members_with_ext.tsv",
               sep="\t",
               index=False)