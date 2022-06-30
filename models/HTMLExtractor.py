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
        time.sleep(4)
        page = driver.page_source
        soup = BeautifulSoup(page, 'lxml')

        return soup
    
    def get_href_from_url(self, driver, url):
        '''
        Função que recebe um driver ('plugin' de um navegador) e uma URL:
        retorna uma lista com todos os links disponíveis na URL enviada
        '''
        soup = self.get_soup_from_url(driver, url)
        acm_ending = 'In order to show you the most relevant results, we have omitted some entries'
        scopus_ending = 'Sorry – your search could not be run.'

        for string in soup.stripped_strings:
            if (acm_ending in string) or (scopus_ending in string):
                print('Fim da busca. Msg: ', string)
                return None
    
        all_links = [link.get('href') for link in soup.find_all('a') if link.get('href') is not None]

        return all_links


    def get_text_from_one_url(self, link, source, driver):
        
        soup = self.get_soup_from_url(driver, link)

        # print(soup)
        title = soup.title.text if soup.title else None
        abstract = None
        intro = None
        conclusion = None
        
        if source.lower() == 'scopus':
            abstract = self.get_scopus_abstract(soup)
            intro = self.get_scopus_intro(soup)
            conclusion = self.get_scopus_conclusion(soup)
        elif source.lower() == 'acm':
            abstract = self.get_acm_abstract(soup)
            intro = self.get_acm_intro(soup)
            conclusion = self.get_acm_conclusion(soup)
        else:
            print('Source can only be ACM or Scopus')

        if abstract and intro and conclusion:
            result = {
                'title': title,
                'abstract': abstract,
                'intro': intro,
                'conclusion': conclusion
            }
            return result, soup
        else:
            return None, soup


