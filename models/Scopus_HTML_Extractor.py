from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from unidecode import unidecode
import os

from Papers_Crawler.models.HTMLExtractor import HTMLExtractor



class Scopus_HTML_extractor(HTMLExtractor):
    '''
    Classe que define um extrator de texto a partir de um arquivo HTML
    As classes diferem entre o tipo de website por conta do formato das tags de cada uma das páginas
    O resultado final são 3 strings contendo abstract, introdução e conclusão de cada artigo
    '''
    
    root_Scopus_link = r'https://www.sciencedirect.com'

    def __init__(self, scopus_links) -> None:
        self.scopus_links = scopus_links
        super().__init__()

    def get_scopus_abstract(self, soup):
        abstract = ''
        target = soup.find('h2',text='Abstract')

        if target:
            for sib in target.find_next_siblings():
                if sib.name=="h2":
                    break
                else:
                    # print(sib.text)
                    print('abstract target')
                    abstract = abstract + sib.text
                    return abstract
        else:
            abstract = None
        
        return abstract

    def get_scopus_intro(self, soup):
        intro = ''
        target = soup.find('h2',text='Introduction')

        if target:
            for sib in target.find_next_siblings():
                if sib.name=="h2":
                    break
                else:
                    #print(sib.text)
                    intro = intro + unidecode(sib.text).replace('\n', '') + ' '
                    print('introdução target')
                    return intro
        else:
            intro = None

        return intro
    
    def get_scopus_conclusion(self, soup):
        conclusion = ''
        targets = soup.find_all('h2')

        if targets != None:
            for header in targets:
                #print(header.text)
                if 'Conclusion' in header.text:
                    print('Achou uma conclusão')
                    for sib in header.find_next_siblings():
                        if sib.name=="h2":
                            break
                        else:
                            conclusion = conclusion + sib.text + ' '
                            print('conclusão target')
                            return conclusion
        else:
            conclusion = None

        return conclusion
    
    def get_text_from_all(self, dir_saving_path=None, maxlimit=None):

        dirname = os.path.dirname(__file__)
        saved_results = []
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        j = 0
        for i, link in enumerate(self.scopus_links):
            text = None
            
            if 'article' in link:
                print(f'Link {i}: {link}')
                text, soup = self.get_text_from_one_url(self.root_Scopus_link + link.replace('\n', ''), 'scopus', driver)

            if text:
                j += 1
                saved_results.append(text)
                print(f'Artigos salvos: {j}')

            if dir_saving_path and soup:
                
                saving_path = dir_saving_path + '/Scopus/' + f"{link.replace('/', '_')}.txt"
                saving_path = os.path.join(dirname, saving_path)
                with open(saving_path, "w") as file:
                    file.write(str(soup))

            if maxlimit:
                if i == maxlimit:
                    break
                
        driver.quit()
        return saved_results

