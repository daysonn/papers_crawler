import os
import pandas as pd

from models.LinkSearcher import LinkSearcher 
from models.ACM_HTML_extractor import ACM_HTML_extractor
from models.Scopus_HTML_Extractor import Scopus_HTML_extractor

def get_links_from_files():
    # Ler links a partir dos arquivos para evitar retrabalho

    f_acm = open("acm_link_file.txt", "r")
    acm_links = [link.replace('\n', '') for link in f_acm]

    f_scopus = open("scopus_link_file.txt", "r")
    scopus_links = [link.replace('\n', '') for link in f_scopus]

    print('Quantidade de links ACM extraídos: ', len(acm_links))
    print('Quantidade de links Scopus extraídos: ', len(scopus_links))

    return acm_links, scopus_links

def save_links(acm_links, scopus_links):
    
    textfile = open("acm_link_file.txt", "w")
    for element in acm_links:
        textfile.write(element + "\n")
    textfile.close()

    textfile = open("scopus_link_file.txt", "w")
    for element in scopus_links:
        textfile.write(element + "\n")
    textfile.close()

def get_links(query):

    searcher = LinkSearcher()
    acm_links, scopus_links = searcher.get_links_from_query(query)

    print('Quantidade de links ACM extraídos: ', len(acm_links))
    print('Quantidade de links Scopus extraídos: ', len(scopus_links))

    return acm_links, scopus_links

query = "sustainability esg"

# acm_links, scopus_links = get_links(query)
# save_links(acm_links, scopus_links)

acm_links, scopus_links = get_links_from_files()

saving_path = '../resources' # os.path.join(dirname, './Resources/HTML/ACM')

# acm_extractor = ACM_HTML_extractor(acm_links)
# acm_papers_text = acm_extractor.get_text_from_all(saving_path, maxlimit=None)
acm_papers_text = []

scopus_extractor = Scopus_HTML_extractor(scopus_links)
scopus_papers_text = scopus_extractor.get_text_from_all(saving_path, maxlimit=None)

papers_text = acm_papers_text + scopus_papers_text

print(len(papers_text))

df = pd.DataFrame(papers_text)
print(df.tail())

dirname = os.path.dirname(__file__)
saving_path = './resources/papers_results.csv' 
saving_path = os.path.join(dirname, saving_path)
df.to_csv(saving_path)

print(f'Total de artigos salvos: {len(papers_text)} com a query {query}')