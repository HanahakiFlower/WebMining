import scrapy

class topjogos(scrapy.Spider):
    name = "wikipedia"
    # allowed_domains = ["wikipedia.org"]
    start_urls = ["https://pt.wikipedia.org/wiki/Lista_de_jogos_eletr%C3%B4nicos_mais_vendidos"]

    
    custom_settings = {
        'FEEDS': { '1_bases_originais/baseoriginal.csv': { 'format': 'csv',}}
        }

    def parse(self, response):
        titulos = response.css('td:nth-child(2) i a::text').getall()
        qtd_vendas = response.css('td:nth-child(3)::text').getall()
        count = 1

        for i in response.css('tr')[1:]: # Pula o primeiro elemento tr, que é a barra com os nomes das colunas
            yield{    
                'Rank': count,
                'Titulo': i.css('td:nth-child(2) a::text').get(),
                'Vendas': i.css('td:nth-child(3)::text').get(),
                'Lancamento' : i.css('td:nth-child(5)::text').get(),
                'Desenvolvedora' : i.css('td:nth-child(6) a::text').get()
            }
            count+=1
        pass
        return dict