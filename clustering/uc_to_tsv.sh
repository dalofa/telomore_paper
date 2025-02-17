cat vclust.ID.72.length.90.uc | cut -f1 > type.txt
cat vclust.ID.72.length.90.uc | cut -f2 > cluster.txt
cat vclust.ID.72.length.90.uc | cut -f9 > seq_name.txt
paste seq_name.txt cluster.txt type.txt > simplified_uc_file.tsv
rm seq_name.txt cluster.txt type.txt
