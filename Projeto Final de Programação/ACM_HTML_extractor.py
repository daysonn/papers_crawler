from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import unidecode

import HTMLExtractor


class ACM_HTML_extractor(HTMLExtractor):
    '''
    Classe que define um extrator de texto a partir de um arquivo HTML
    As classes diferem entre o tipo de website por conta do formato das tags de cada uma das páginas
    O resultado final são 3 strings contendo abstract, introdução e conclusão de cada artigo
    '''
    
    def get_acm_abstract(soup):
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
    
    def get_acm_intro(soup):
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
    
    def get_acm_conclusion(soup):
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
    
    def get_text_from_url(self, link, source):
        
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        
        soup = self.get_soup_from_url(driver, link)
        print(soup)
        title = soup.title.text if soup.title else None
        abstract = None
        intro = None
        conclusion = None
        
        if source.lower() == 'scopus':
            abstract = get_scopus_abstract(soup)
            intro = get_scopus_intro(soup)
            conclusion = get_scopus_conclusion(soup)
        elif source.lower() == 'acm':
            abstract = get_acm_abstract(soup)
            intro = get_acm_intro(soup)
            conclusion = get_acm_conclusion(soup)
        else:
            print('Source can only be ACM or Scopus')

        self.driver.quit()

        if abstract and intro and conclusion:
            result = {
                'title': title,
                'abstract': abstract,
                'intro': intro,
                'conclusion': conclusion
            }
            return result
        else:
            return None