import scrapy
from scrapy.http import FormRequest

class ExampleSpider(scrapy.Spider):
    name = 'PostSpider'
    allowed_domains = ['zencheck.com.br']

    def start_requests(self):
        params = {
            "Usuario":"igorsimoes",   
            "Senha":"je123!"
            }
        yield FormRequest('https://zencheck.com.br/Extintor/Login/Login', callback=self.parse,
                                 method='POST', formdata=params)
        

    def parse(self, response):
        print("Esta é a resposta: "+response.text)
        pass