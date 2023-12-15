# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 13:48:30 2023

@author: bianca
"""



import requests

timelimit_sec = 15

# Custom exception for the timeout
class TimeoutException(Exception):
    pass


srn_api_url = "https://api.sustainabilityreportingnavigator.com/api/"

def get_srn_companies():
    """
    Returns a list of companies that are included in SRN Document Database.
    Returns:
        [list{dict}]: A list containg company level metadata
    """
    response = requests.get(srn_api_url + "companies")
    return response.json()


def get_srn_documents():
    """
    Returns a list of documents that are included in SRN Document Database.
    Returns:
        [list{dict}]: A list containg document level metadata
    """
    response = requests.get(srn_api_url + "documents")
    return response.json()


def download_document(id, filename, timeout=timelimit_sec):
    """
    Retreives a certain document from the SRN Document Database and 
    stores it at the provided file path.
    Args:
        id (str): The SRN document id.
        fpath (str): A sting contains the file path where you want to
            store the file.
        timeout (int, optional): Sometimes, a download API call might
            nlock because of a dying connection or because the data
            is not available. If a timeout is reached, the according
            API request will raise an exception and exit. 
            Defaults to 60 seconds.
    """
    response = requests.get(
        srn_api_url + f"documents/{id}/download", 
        timeout=timeout
    )
    with open("./data/reports_eu/"+filename+".pdf", 'wb') as f: f.write(response.content)
   
    
    
if __name__ == "__main__":
    companies = get_srn_companies()
    documents = get_srn_documents()
  #  filename = "" 
    for document in documents:
        company = [c for c in companies if document['company_id'] == c['id']]
        isin = ""
        if company == []:
            isin = "no_company"
        else:
            isin = company[0]['isin']
        filename = isin + "_" + document['year'] + "_" + document['type']
        print(filename)
        try:
            download_document(document['id'], filename)
        except:
            with open("Missing_files.txt", "a") as myfile:
               myfile.write(document['id'] + "\n")
            continue

       
        
    """   
    print("Searching company with a name containing 'Allianz'")
    matches = [c for c in companies if 'Allianz' in c['name']]
    print(
        "Found {len(matches)} match(es). " +
        "Retrieving the documents for the first match."
    )
    docs = [d for d in documents if d['company_id'] == matches[0]['id']] 
    FPATH = 'test_srn_docs.pdf'
    print(
        "Found {len(docs)} documents. " +
        "Retrieving the first document from the list " +
        "and storing it as '{FPATH}'."
    )
 
    """
    print("done!")
   