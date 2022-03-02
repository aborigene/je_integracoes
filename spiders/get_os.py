# ESTE É UM TRABALHO EM PROGRESSO. O SCRIPT AINDA NÃO COLETA OU CRIA OS, POR EQUANTO APENAS FAZ O POST DO LOGIN E CARREGA A PRINCIPAL

from asyncio.windows_events import NULL
from http import cookiejar
import scrapy
from scrapy.http import FormRequest
import json
import re

class ExampleSpider(scrapy.Spider):
    name = 'GetOS'
    allowed_domains = ['zencheck.com.br']
    cookie_jar = NULL
    cookie = NULL

    def start_requests(self):
        yield scrapy.Request("https://zencheck.com.br/Extintor/Login",
                                meta={'cookiejar': self.cookie_jar}, 
                                callback=self.handleNetSessionID,
                                method='GET')
        #yield FormRequest('https://zencheck.com.br/Extintor/Login/Login', meta={'cookiejar': self.cookie_jar}, callback=self.redirectPrincipal,
        #                         method='POST', formdata=params)
        
    def handleNetSessionID(self, response):
        print("Handling .NetSessionID")
        self.cookie = response.headers.getlist('Set-Cookie')
        rawAspnetSessionId = str(self.cookie[0])
        print(rawAspnetSessionId)
        aspnetSessionId = re.findall("^b'ASP.NET_SessionId=(.*); path", rawAspnetSessionId)
        print(aspnetSessionId)

        print("Handling Zencheck Login")

        params = {
            "Usuario":"igorsimoes",   
            "Senha":"je123!"
            }
        yield FormRequest('https://zencheck.com.br/Extintor/Login/Login', 
                            meta={'cookiejar': self.cookie_jar}, 
                            callback=self.redirectPrincipal,
                            cookies={"ASP.NET_SessionId": aspnetSessionId[0]},
                            method='POST', 
                            formdata=params)

    #def zencheckLogin(self):
        

    def redirectPrincipal(self, response):
        print("Handling Redirect to Principal")
        self.cookie = response.headers.getlist('Set-Cookie')
        parsed_response = json.loads(response.text)
        print("Resposta Login: "+response.text)
        print("Redirect URL:"+parsed_response["url"])
        yield scrapy.Request("https://zencheck.com.br"+parsed_response["url"],
                                meta={'cookiejar': self.cookie_jar}, 
                                cookies=self.cookie,
                                callback=self.listaOS,
                                method='GET')
        pass

    def parseHTML(self, response):
        self.cookie = response.headers.getlist('Set-Cookie')
        #parsed_response = json.loads(response.text)
        print("Resposta HTML: "+response.text)
        pass

    def listaOS(self, response):
        print("Resposta Principal: "+response.text)
        self.cookie = response.headers.getlist('Set-Cookie')
        #parsed_response = json.loads(response.text)
        
        yield scrapy.Request("https://zencheck.com.br/Extintor/Oficina/OrdemDeServicoDoExtintor", 
                                meta={'cookiejar': self.cookie_jar}, 
                                cookies=self.cookie,
                                callback=self.parseHTML,
                                method='GET')
        pass