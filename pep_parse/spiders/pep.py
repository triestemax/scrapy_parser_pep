import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_href_pep = response.css("a.pep::attr('href')").getall()
        for pep_url in all_href_pep:
            yield response.follow(pep_url, callback=self.parse_pep)

    def parse_pep(self, response):
        raw = response.css('h1.page-title::text').get().split(' – ')
        data = {
            'number': raw[0][4:],
            'name': raw[1],
            'status': response.css('dt:contains("Status") + dd::text').get()
        }
        yield PepParseItem(data)
