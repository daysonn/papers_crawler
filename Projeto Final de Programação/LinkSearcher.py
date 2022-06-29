from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

import HTMLExtractor

class LinkSearcher(HTMLExtractor):
    def __init__ (self):
        pass
    
    def get_links_from_query(self, query):
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        
        acm = self.get_ACM_links_from_query(query)
        scopus = self.get_Scopus_links_from_query(query)
        
        self.driver.quit()
        
        return acm, scopus
    
    def get_valid_links_per_Scopus_page(self, all_links):
        '''
        Função que recebe uma lista de links extraídos de uma page HTML:
        retorna uma lista apenas com links válidos que possuem um paper em formato HTML da Scopus
        '''

        valid_links = [link for link in all_links if link.startswith("/science/") and not link.endswith(".pdf")]

        return valid_links
    
    def get_Scopus_links_from_query(self, query):
        '''
        Função que itera sobre uma query inicial na Scopus 
        e gera uma lista de links únicos e válidos da Scopus 

        '''

        query = '%20'.join(query.split())
        url = "https://www.sciencedirect.com/search?qs=" + query + '&show=100'
        next_page_link = url
        papers_links = []
        offset = 100
        i=0
        # Enquanto houver uma próxima página válida
        while(next_page_link != None):

            # Busca todos os links da página
            all_links = self.get_href_from_url(next_page_link) 
            if all_links:

                # Recebe uma lista de links válidos
                valid_links= self.get_valid_links_per_Scopus_page(all_links) 

            else:
                break

            # Adiciona links válidos na lista e monta a próxima página
            papers_links = papers_links + valid_links
            next_page_link = url + '&offset=' + str(offset)
            offset += 100
            
            i += 1
            if i>2:
                break

        return set(papers_links)

    
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
    
    def get_valid_links_per_ACM_page(self, all_links):
        '''
        Função que recebe uma lista de links extraídos de uma page HTML:
        retorna uma lista apenas com links válidos que possuem um paper em formato HTML da Scopus
        '''

        valid_links = [link for link in all_links if "/fullHtml/" in link]   
        return valid_links
    
    def get_ACM_links_from_query(self, query):
        '''
        Gera uma lista de links válidos a serem consultados a partir de uma query
        e itera sobre as páginas de resultados 
        '''

        query = '+'.join(query.split())
        url = "https://dl.acm.org/action/doSearch?AllField=" + query
        page = '&startPage='
        page_size = "&pageSize=20"
        offset = 0

        next_page_link = url + page + str(offset) + page_size
        papers_links = []
        i=0

        # Enquanto houver uma próxima página válida
        while(next_page_link != None):

            # Busca todos os links da página
            all_links = self.get_href_from_url(next_page_link) 

            if all_links:

                # Recebe uma lista de links e 
                # retorna os viáveis + o link da próxima página
                valid_links= self.get_valid_links_per_ACM_page(all_links) 

            else:
                break

            #Adiciona links válidos na lista
            papers_links = papers_links + valid_links
            offset += 1
            next_page_link = url + page + str(offset) + page_size
            
            i += 1
            if i>2:
                break

        return set(papers_links)