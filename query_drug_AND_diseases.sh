disease_list="diseaselist.txt"
druglist_list="druglist.txt"
top_n=-1 # -1 to get all

python query_drug_AND_diseases.py "$disease_list" "$druglist_list" "$top_n"