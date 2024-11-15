from Bio import Entrez
import pandas as pd

def query_pubmed(query_text, email="your_email@example.com", max_results=-1):
    """
    Query PubMed with the given text and return matched articles, saved as a JSON file.

    Parameters:
    query_text (str): The search term or query for PubMed.
    email (str): Your email address for NCBI (required).
    max_results (int): Maximum number of articles to retrieve. Set to -1 to retrieve all.

    Returns:
    records (list): A list of dictionaries, where each dictionary contains details of an article.
    """
    Entrez.email = email  # Set the email for Entrez
    
    # Initial search to get the total count of results
    search_handle = Entrez.esearch(db="pubmed", term=query_text, retmax=1)
    search_results = Entrez.read(search_handle)
    search_handle.close()
    
    total_results = int(search_results["Count"])
    
    # If max_results is -1, retrieve all available results
    if max_results == -1:
        max_results = total_results
    
    # Search for the specified number of results
    search_handle = Entrez.esearch(db="pubmed", term=query_text, retmax=max_results)
    search_results = Entrez.read(search_handle)
    search_handle.close()

    # Get list of PubMed IDs from search results
    id_list = search_results["IdList"]
    if not id_list:
        print("No articles found.")
        return  None # Exit if no articles found

    # Fetch article details for each PubMed ID
    fetch_handle = Entrez.efetch(db="pubmed", id=id_list, rettype="medline", retmode="text")
    article_details = fetch_handle.read()
    fetch_handle.close()

    # Parsing articles and storing details in a list of dictionaries
    records = []
    for record in article_details.split("\n\n"):  # Each article record is separated by a newline
        if record:
            article = {"Authors": [], "Keywords": []}
            # append query_text to article
            article["Query"] = query_text
            in_abstract = False
            abstract_lines = []
            for line in record.split("\n"):
                if line.startswith("PMID- "):
                    article["PMID"] = line.replace("PMID- ", "PMID:").strip()
                elif line.startswith("TI  - "):
                    article["Title"] = line.replace("TI  - ", "").strip()
                elif line.startswith("AB  - "):
                    # Start of an abstract section
                    in_abstract = True
                    abstract_lines.append(line.replace("AB  - ", "").strip())
                elif in_abstract and line.startswith("      "):
                    # Continuation of the abstract
                    abstract_lines.append(line.strip())
                else:
                    in_abstract = False  # End of abstract field

                if line.startswith("AU  - "):
                    article["Authors"].append(line.replace("AU  - ", "").strip())
                elif line.startswith("DP  - "):
                    article["Date"] = line.replace("DP  - ", "").strip()
                elif line.startswith("JT  - "):
                    article["Journal"] = line.replace("JT  - ", "").strip()
                elif line.startswith("MH  - "):  # Keywords in PubMed are under the 'MH' tag
                    article["Keywords"].append(line.replace("MH  - ", "").strip())

            # Combine abstract lines into a single string
            article["Abstract"] = " ".join(abstract_lines)
            records.append(article)

    return records
