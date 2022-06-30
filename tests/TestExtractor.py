from Papers_Crawler.models.LinkSearcher import LinkSearcher 
from Papers_Crawler.models.ACM_HTML_extractor import ACM_HTML_extractor
from Papers_Crawler.models.Scopus_HTML_Extractor import Scopus_HTML_extractor



class TestExtractor():
    '''
    Classe que efetua bateria de testes da aplicação de extração de artigos web.
    Os testes unitários incluem checagem dos tipos e validação de conteúdo dos links dos artigos na primeira função.
    Na segunda, alguns links da scopus são mockados artificialmente para diminuir o tempo de retorno dos testes. Nesse caso,
    os testes incluem checagem de tipo e validação das chaves dos dicionários enviados pelo extrator de textos.
    '''
    
    def testPapersLinks(self):

        query = "sustainability"
        searcher = LinkSearcher()
        acm_links, scopus_links = searcher.get_links_from_query(query, max_pages_limit=1)

        assert isinstance(acm_links, list)
        assert isinstance(scopus_links, list)

        assert isinstance(acm_links[0], str)
        assert isinstance(scopus_links[0], str)

        assert acm_links[0].startswith('/doi/fullHtml/')
        assert scopus_links[0].startswith('/science/')

    def testPapersText(self):

        scopus_links = [
            '/science/article/pii/S136454392200048X',
            '/science/article/pii/S2772390922000166',
            '/science/article/pii/S1877050920320615',
            '/science/article/pii/S0377221720300400'
        ]
        saving_path = '../resources'

        scopus_extractor = Scopus_HTML_extractor(scopus_links)
        scopus_papers_text = scopus_extractor.get_text_from_all(saving_path, maxlimit=5)
        #print(scopus_papers_text)

        assert isinstance(scopus_papers_text, list)
        assert len(scopus_papers_text) <= 5

        first_result = scopus_papers_text[0]
        assert isinstance( first_result, dict)

        keys = ['title', 'abstract', 'intro', 'conclusion']
        assert list(first_result.keys()) == keys
        
        assert first_result['title'] is not None
        assert first_result['abstract'] is not None
        assert first_result['intro'] is not None
        assert first_result['conclusion'] is not None
        

        