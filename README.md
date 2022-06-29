# papers_crawler
Projeto para extração de texto de artigos disponibilizados em formato HTML nos repositórios Scopus e ACM.

Este projeto tem como objetivo extrair abstract, introdução e conclusão de papers científicos disponibilizados em formato HTML. A partir de uma query em linguagem natural, nós remontamos a URL de busca da Scopus e da ACM para encontrar artigos que estão em formato HTML, possibilitando a extração por seção.

Em alguns passos, o funcionamento do 

  1- Remontar a URL de busca a partir de uma query
  2- Buscar a lista de URLs válidas com papers em HTML
  3- Acessar URL por URL, inspecionar HTML e extrair abstract, introdução e conclusão com base na estrutura dos próprios artigos
  4- Salvar esses textos localmente
  

