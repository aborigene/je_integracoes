import scrapy
from scrapy.http import FormRequest
import json

class ExampleSpider(scrapy.Spider):
    name = 'PostSpider'
    allowed_domains = ['zencheck.com.br']

    def start_requests(self):
        params = {
            "Usuario":"igorsimoes",   
            "Senha":"je123!"
            }
        yield FormRequest('https://zencheck.com.br/Extintor/Login/Login', callback=self.redirectPrincipal,
                                 method='POST', formdata=params)
        

    def redirectPrincipal(self, response):
        parsed_response = json.loads(response.text)
        print("Resposta Login: "+response.text)
        print("Redirect URL:"+parsed_response["url"])
        yield scrapy.Request("https://zencheck.com.br"+parsed_response["url"], callback=self.parsePrincipal,
                                 method='GET')
        pass

    def parsePrincipal(self, response):
        #parsed_response = json.loads(response.text)
        print("Resposta Principal: "+response.text)
        pass