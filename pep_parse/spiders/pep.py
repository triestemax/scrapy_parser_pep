import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_href_pep = response.css("a.pep::attr('href')").getall()
        for pep_url in all_href_pep:
            pep_url += '/'
            yield response.follow(pep_url, callback=self.parse_pep)

    def parse_pep(self, response):
        # сплитим по такому знаку ' - ' у меня все норм отробажается
        raw = response.css('h1.page-title::text').get().split(' – ')
        '''
        да, в подсказке такое
        .css('dt:contains("Status") + dd::text').get()
        ,но когда использую у меня выводит пустую строку.
        Не знаю почему такая фигня...
        С этим и бился с 29.12, чтоб ловил правильно статус,
        смог только конструкцией ниже.
        '''
        status_raw = response.css('dt:contains("Status") + dd')
        status = status_raw.css('abbr::text').get()

        data = {
            'number': raw[0][4:],
            'name': raw[1],
            'status': status,
        }
        yield PepParseItem(data)
