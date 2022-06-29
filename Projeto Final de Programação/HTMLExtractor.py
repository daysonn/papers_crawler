from bs4 import BeautifulSoup
import time

class HTMLExtractor():
    
    def __init__ (self):
        pass
    
    def get_soup_from_url(self, driver, url):
        '''
        Função que recebe um driver ('plugin' que simula um navegador) e uma URL:
        retorna uma página em formato HTML para extração dos dados
        '''
        
        driver.get(url)
        time.sleep(3)
        page = self.driver.page_source
        soup = BeautifulSoup(page, 'lxml')

        return soup
    
    def get_href_from_url(self, url):
        '''
        Função que recebe um driver ('plugin' de um navegador) e uma URL:
        retorna uma lista com todos os links disponíveis na URL enviada
        '''
        soup = self.get_soup_from_url(url)
        acm_ending = 'In order to show you the most relevant results, we have omitted some entries'
        scopus_ending = 'Sorry – your search could not be run.'

        for string in soup.stripped_strings:
            if (acm_ending in string) or (scopus_ending in string):
                print('Fim da busca. Msg: ', string)
                return None
    
        all_links = [link.get('href') for link in soup.find_all('a') if link.get('href') is not None]

        return all_links