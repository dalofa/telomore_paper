"""Convert clstr-file to table for R"""


def clstr_to_table(clstr_file, output_file):
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

clstr_to_table("tap_cluster/clusters_0.70.clstr","tables/tap_70_cluster.tsv")
clstr_to_table("tpg_cluster/clusters_0.70.clstr","tables/tpg_70_cluster.tsv")
clstr_to_table("tac_cluster/clusters_0.70.clstr","tables/tac_70_cluster.tsv")
clstr_to_table("tpc_cluster/clusters_0.70.clstr","tables/tpc_70_cluster.tsv")
clstr_to_table("gtpA_cluster/clusters_0.70.clstr","tables/gtpA_70_cluster.tsv")
clstr_to_table("gtpB_cluster/clusters_0.70.clstr","tables/gtpB_70_cluster.tsv")


