from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import unidecode

import HTMLExtractor



class Scopus_HTML_extractor(HTMLExtractor):
    '''
    Classe que define um extrator de texto a partir de um arquivo HTML
    As classes diferem entre o tipo de website por conta do formato das tags de cada uma das páginas
    O resultado final são 3 strings contendo abstract, introdução e conclusão de cada artigo
    '''
    
    def get_scopus_abstract(soup):
        abstract = ''
        target = soup.find('h2',text='Abstract')

        if target:
            for sib in target.find_next_siblings():
                if sib.name=="h2":
                    break
                else:
                    #print(sib.text)
                    abstract = abstract + sib.text
        else:
            abstract = None

        return abstract

    def get_scopus_intro(soup):
        intro = ''
        target = soup.find('h2',text='Introduction')

        if target:
            for sib in target.find_next_siblings():
                if sib.name=="h2":
                    break
                else:
                    #print(sib.text)
                    intro = intro + unidecode(sib.text).replace('\n', '') + ' '
        else:
            intro = None

        return intro
    
    def get_scopus_conclusion(soup):
        conclusion = ''
        targets = soup.find_all('h2')

        if targets != None or len(targets) != 0:
            for header in targets:
                if '. Conclusion' in header.text:
                    for sib in header.find_next_siblings():
                        if sib.name=="h2":
                            break
                        else:
                            conclusion = conclusion + sib.text + ' '
        else:
            conclusion = None

        return conclusion
    
    def get_text_from_url(soup, source):
        title = soup.title.text
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