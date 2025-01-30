from scr.query import query_pubmed
import sys
import pandas as pd
import json
import time

if __name__ == "__main__":
    query_disease_list_file = sys.argv[1]  # required parameter
    query_drug_list_file = sys.argv[2]  # required parameter
    if len(sys.argv) > 3:
        number_of_articles = int(sys.argv[3])  # optional parameter
    else:
        number_of_articles = -1

    # Read query_drug_list_file
    with open(query_drug_list_file) as f:
        query_drug_list = f.readlines()
    query_drug_list = [x.strip() for x in query_drug_list]  # Remove whitespace
    query_drug_list = list(set(query_drug_list))  # Remove duplicates

    # Read query_disease_list_file
    with open(query_disease_list_file) as f:
        query_disease_list = f.readlines()
    query_disease_list = [x.strip() for x in query_disease_list]
    query_diseases = "OR".join(["(" + x + ")" for x in query_disease_list])

    list_of_records = []
    
    for query_drug in query_drug_list:
        query_text = f"({query_drug})AND({query_diseases})"
        print("Querying:", query_text)
        
        attempts = 0
        while True:
            try:
                records = query_pubmed(query_text, max_results=number_of_articles)
                if records is not None:
                    for record in records:
                        record["Query_disease"] = query_diseases
                        record["Query_drug"] = query_drug
                    list_of_records.extend(records)
                break  # Exit loop on success
            except Exception as e:
                attempts += 1
                print(f"Error occurred: {e}. Retrying in 60 seconds... (Attempt {attempts})")
                time.sleep(60)
        
    # Convert list of dictionaries to JSON
    json_records = json.dumps(list_of_records, indent=4)
    with open("out.json", "w") as f:
        f.write(json_records)
    
    # Write to TSV
    if list_of_records:
        df = pd.DataFrame(list_of_records)
        df = df[['Query_disease', 'Query_drug', 'PMID', 'Query']]
        df.to_csv("out.tsv", sep="\t", index=False)
