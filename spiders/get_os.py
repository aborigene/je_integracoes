from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import FormRequest
import scrapy

class LoginSpider(scrapy.Spider):
    name = 'get_os'
    allowed_domains = ['zenchech.com.br']
    start_urls = ['https://zencheck.com.br/Extintor/Login/Login']

def start_requests(self):
   return [
      FormRequest("zencheck.com.br/Extintor/Login/Login", formdata={"Usuario":"igorsimoes",   
           "Senha":"je123!",
           "X-Requested-With":"XMLHttpRequest"}, callback=self.parse)]

def parse(self,response):
    print(response)
    pass
#class ImdbCrawler(CrawlSpider):
#    name = 'imdb'
#    allowed_domains = ['www.imdb.com']
#    start_urls = ['https://www.imdb.com/']
#    rules = (Rule(LinkExtractor()),)

