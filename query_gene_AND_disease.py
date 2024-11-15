from pubmed.query import query_pubmed
import sys
import pandas as pd
import json


if __name__ == "__main__":
    querry_disease = sys.argv[1] # required parameter
    query_gene_list_file = sys.argv[2] # required parameter
    if len(sys.argv) > 3:
        number_of_articles = sys.argv[3] # optional parameter
    else:
        number_of_articles = -1

    # read query_gene_list_file
    with open(query_gene_list_file) as f:
        query_gene_list = f.readlines()
    # remove whitespace characters like `\n` at the end of each line
    query_gene_list = [x.strip() for x in query_gene_list]
    
    list_of_records = []

    for query_gene in query_gene_list:
        query_text = "(" + querry_disease + ")AND(" + query_gene + ")"
        print("Querying:", query_text)
        records = query_pubmed(query_text, max_results=number_of_articles)
        if records is None:
            continue
        # add query_disease and Query_gene to all entries in records
        for record in records:
            record["Query_disease"] = querry_disease
            record["Query_gene"] = query_gene
        list_of_records.extend(records)

    # Convert list of dictionaries to json
    json_records = json.dumps(list_of_records, indent=4)
    # write to file
    with open("out.json", "w") as f:
        f.write(json_records)
    
    # write to tsv
    df = pd.DataFrame(list_of_records)
    # subset columns ['Query_disease', 'Query_gene', 'PMID']
    df = df[['Query_disease', 'Query_gene', 'PMID', 'Query']]
    df.to_csv("out.tsv", sep="\t", index=False)
    


