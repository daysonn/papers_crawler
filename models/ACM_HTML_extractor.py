from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from unidecode import unidecode
import os

from Papers_Crawler.models.HTMLExtractor import HTMLExtractor


class ACM_HTML_extractor(HTMLExtractor):
    '''
    Classe que define um extrator de texto a partir de um arquivo HTML
    As classes diferem entre o tipo de website por conta do formato das tags de cada uma das páginas
    O resultado final são 3 strings contendo abstract, introdução e conclusão de cada artigo
    '''

    root_ACM_link = r'https://dl.acm.org'

    def __init__(self, acm_links) -> None:
        self.acm_links = acm_links
        super().__init__()
    
    def get_acm_abstract(self, soup):
        abstract = ''
        target = soup.find(class_="abstract")

        if target:
            for sib in target.children: #find_next_siblings():
                if sib.name=="h2":
                    break
                else:
                    abstract = abstract + unidecode(sib.text).replace('\n', '') + ' '
        else:
            abstract = None

        return abstract
    
    def get_acm_intro(self, soup):
        intro = ''
        save_header = None
        targets = soup.find_all('h2')
        to_stop = False

        if targets != None or len(targets) != 0:
            for header in targets:
                if 'introduction' in header.text.lower():
                    save_header = header

            if save_header:    
                while(save_header.name != 'header'):
                    save_header = save_header.parent

                for sib in save_header.find_next_siblings():
                    if to_stop:
                        print('parou ao encontrar: ', sib.text)
                        break
                    elif sib.name=="h2":
                        to_stop = True                
                    elif sib.text not in intro:
                        intro = intro + unidecode(sib.text).replace('\n', '') + ' '
        else:
            intro = None

        return intro
    
    def get_acm_conclusion(self, soup):
        conclusion = ''
        save_header = None
        targets = soup.find_all('h2')
        to_stop = False

        if targets != None or len(targets) != 0:
            for header in targets:
                if 'conclusion' in header.text.lower():
                    save_header = header

            if save_header:    
                while(save_header.name != 'header'):
                    save_header = save_header.parent

                for sib in save_header.find_next_siblings():
                    if to_stop:
                        print('parou ao encontrar: ', sib.text)
                        break
                    elif sib.name=="h2":
                        to_stop = True                
                    elif sib.text not in conclusion:
                        conclusion = conclusion + unidecode(sib.text).replace('\n', '') + ' '
        else:
            conclusion = None

        return conclusion

    def get_text_from_all(self, dir_saving_path=None, max_limit_search=None):

        dirname = os.path.dirname(__file__)
        saved_results = []
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        j = 0
        for i, link in enumerate(self.acm_links):
            print(f'Link {i}: {link}')
            #self.get_soup_from_url(driver, url)
            text, soup = self.get_text_from_one_url(self.root_ACM_link + link.replace('\n', ''), 'acm', driver)

            if text:
                saved_results.append(text)

                if dir_saving_path and soup:
                    j += 1
                    saving_path = dir_saving_path + '/ACM/' + f"{link.replace('/', '_')}.txt"
                    saving_path = os.path.join(dirname, saving_path)

                    with open(saving_path, "w") as file:
                        file.write(str(soup))
            if max_limit_search:
                if j == max_limit_search:
                    break
        driver.quit()
        return saved_results

        