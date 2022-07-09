import scrapy
import json
from pathlib import Path
import os

class MovieSpider(scrapy.Spider):
    name = "imdb"
    path = Path('.')
    tmp_storage = path / 'tmp'
    tmp_storage.mkdir(exist_ok=True)

    def start_requests(self):
        urls = [
            'https://www.imdb.com/feature/genre/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.xpath('//*[@id="main"]/div[6]/span/div/div/div/div/div/div/div/div/a/text()').getall()
        links = response.xpath('//*[@id="main"]/div[6]/span/div/div/div/div/div/div/div/div/a/@href').getall()
        # remove trailing whitespaces
        title = list(map(str.strip, title))

        for link in links:
            yield response.follow(link, self.parse_movie)

    def parse_movie(self, response):
        links = response.xpath('//*[@id="main"]/div/div[3]/div/div/div[3]/h3/a/@href').getall()
        links = list(map(response.urljoin, links))
        with open(self.tmp_storage / 'test.txt', 'a') as f:
            f.writelines(f'{link}\n' for link in links)
        next_names = response.xpath('//*[@id="main"]/div/div[1]/div[2]/a/text()').getall()
        next_links = response.xpath('//*[@id="main"]/div/div[1]/div[2]/a/@href').getall()
        _val = response.xpath('//*[@id="main"]/div/div[1]/div[2]/span[1]/text()').get()
        _header = response.xpath('//*[@id="main"]/div/h1/text()').get()
        print(f"saving {_header}: {_val}")
        for idx, nxt in enumerate(next_names):
            if nxt == 'Next »':
                yield response.follow(next_links[idx], self.parse_movie)