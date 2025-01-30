from scr.query import query_pubmed
import sys
import pandas as pd
import json


if __name__ == "__main__":
    query_disease_list_file = sys.argv[1] # required parameter
    query_drug_list_file = sys.argv[2] # required parameter
    if len(sys.argv) > 3:
        number_of_articles = int(sys.argv[3]) # optional parameter
    else:
        number_of_articles = -1

    # read query_drug_list_file
    with open(query_drug_list_file) as f:
        query_drug_list = f.readlines()
    # remove whitespace characters like `\n` at the end of each line
    query_drug_list = [x.strip() for x in query_drug_list]
    # remove duplicates
    query_drug_list = list(set(query_drug_list))

    # read query_disease_list_file
    with open(query_disease_list_file) as f:
        query_disease_list = f.readlines()
    # remove whitespace characters like `\n` at the end of each line
    query_disease_list = [x.strip() for x in query_disease_list]
    # asemble query_diseases as (Disease1)OR(Disease2)OR(Disease3)
    query_diseases = "OR".join(["(" + x + ")" for x in query_disease_list])
    
    list_of_records = []

    for query_drug in query_drug_list:
        query_text = "(" + query_drug + ")AND(" + query_diseases + ")"
        print("Querying:", query_text)
        records = query_pubmed(query_text, max_results=number_of_articles)
        if records is None:
            continue
        # add query_disease and Query_gene to all entries in records
        for record in records:
            record["Query_disease"] = query_diseases
            record["Query_drug"] = query_drug
        list_of_records.extend(records)

    # Convert list of dictionaries to json
    json_records = json.dumps(list_of_records, indent=4)
    # write to file
    with open("out.json", "w") as f:
        f.write(json_records)
    
    # write to tsv
    df = pd.DataFrame(list_of_records)
    # subset columns ['Query_disease', 'Query_gene', 'PMID']
    df = df[['Query_disease', 'Query_drug', 'PMID', 'Query']]
    df.to_csv("out.tsv", sep="\t", index=False)
    


