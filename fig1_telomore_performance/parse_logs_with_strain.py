"""
Script for parsing logs into a table
"""
import pandas as pd


########################################
# Illumina logs
########################################
left_ext=[]
right_ext=[]
col_info = []
log_start=False

# Parse Illumina log files
with open("ill_logs_with_header.txt") as log_file:
    for line in log_file.readlines():
        
        # get strain_name
        if line.startswith("NBC"):
            strain=line.replace("\n","")
        
        # get replicon
        if line.startswith("CP"):
            replicon=line.replace("\n","")
        if line.startswith("FINAL GENOME EXTENSION"):
            log_start=True
        # Add line if this is the final genome ext. field
        elif line.startswith("left_cons") & log_start:
            f = line.replace("\n","")
            
            left =f.split("\t")[0]
            right =f.split("\t")[1] 
            left_num = left.split(":")[1]
            right_num = right.split(":")[1]
            

            left_ext.append(left_num)
            right_ext.append(right_num)
            col_info.append([strain,
                             replicon,
                             left_num,
                             right_num])
            # reset to only get final ext fields
            log_start=False

ill_ext = pd.DataFrame(col_info,
                       columns = ["strain",
                                  "replicon",
                                  "left_ext",
                                  "right_ext"])

ill_ext.to_csv(path_or_buf = "ill_ext_header.tsv",
               sep="\t",
               index=False)


########################################
# NP logs
########################################
left_ext=[]
right_ext=[]
col_info = []
log_start=False

# Parse Illumina log files
with open("np_logs_with_header.txt") as log_file:
    for line in log_file.readlines():
        
        # get strain_name
        if line.startswith("NBC"):
            strain=line.replace("\n","")
        
        # get replicon
        if line.startswith("CP"):
            replicon=line.replace("\n","")
        if line.startswith("FINAL GENOME EXTENSION"):
            log_start=True
        # Add line if this is the final genome ext. field
        elif line.startswith("left_cons") & log_start:
            f = line.replace("\n","")
            
            left =f.split("\t")[0]
            right =f.split("\t")[1] 
            left_num = left.split(":")[1]
            right_num = right.split(":")[1]
            

            left_ext.append(left_num)
            right_ext.append(right_num)
            col_info.append([strain,
                             replicon,
                             left_num,
                             right_num])
            # reset to only get final ext fields
            log_start=False

NP_ext = pd.DataFrame(col_info,
                       columns = ["strain",
                                  "replicon",
                                  "left_ext",
                                  "right_ext"])

NP_ext.to_csv(path_or_buf = "NP_ext_header.tsv",
               sep="\t",
               index=False)


########################################
# Combine logs in table
########################################

# Rename columns before joining
NP_ext = NP_ext.rename(columns={"left_ext": "np_left_ext",
                        "right_ext": "np_right_ext"})
ill_ext = ill_ext.rename(columns={"left_ext": "ill_left_ext",
                        "right_ext": "ill_right_ext"})

# join and sanity check
merged_df = pd.merge(left = ill_ext,
                     right = NP_ext,
                     on="replicon",
                     how="inner")

for strain in merged_df.iterrows():
    strain_x = strain[1][0]
    strain_y = strain[1][4]
    if strain_x!=strain_y:
        print("joining issue")
        exit()

# rename columns
merged_df = merged_df.rename(columns={"strain_x": "strain"})
merged_df = merged_df.drop(["strain_y"], axis=1)

merged_df.to_csv(path_or_buf="comb_NP_and_ill.tsv",
                 sep="\t",
                 index=False)


