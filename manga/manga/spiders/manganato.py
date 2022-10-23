import scrapy
import json
from datetime import datetime

class MangaSpider(scrapy.Spider):
    name = "manga"
    bookmark_path = '/Users/jadenjelu/projects/spiders/manga/manga/bookmarks.json'
    news = False

    def start_requests(self):
        urls = [
            'https://readmanganato.com/manga-ec981811', # Ranker Who Lives A Second Time
            'https://readmanganato.com/manga-dr980474', # Solo Leveling
            'https://readmanganato.com/manga-ci980191', # A Returner's Magic Should Be Special
            'https://readmanganato.com/manga-ml989546', # Leveling With The Gods
            'https://readmanganato.com/manga-dg980989', # The Beginning After The End
            'https://readmanganato.com/manga-hu985229', # The Great Mage Returns After 4000 Years
            'https://readmanganato.com/manga-lu989229', # Reincarnation Of The Suicidal Battle God
            'https://readmanganato.com/manga-jo986949', # Memorize
            'https://readmanganato.com/manga-iw985579', # Omniscient Reader’S Viewpoint
            'https://readmanganato.com/manga-nb990510', # The World After The Fall
            'https://readmanganato.com/manga-ko987549', # Sss-Class Suicide Hunter
            'https://chapmanganato.com/manga-ax951880', # tales of demons and gods
            'https://chapmanganato.com/manga-bf979214', # versatile mage
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.xpath('/html/body/div[1]/div[3]/div[1]/div[2]/div[2]/h1/text()').get()
        most_recent_chapters = response.xpath('/html/body/div[1]/div[3]/div[1]/div[3]/ul/li/a/text()').getall()
        most_recent_times = response.xpath('/html/body/div[1]/div[3]/div[1]/div[3]/ul/li/span/@title').getall()
        links = response.xpath('/html/body/div[1]/div[3]/div[1]/div[3]/ul/li/a/@href').getall()

        # newest chapter
        newest = datetime.strptime(most_recent_times[0], '%b %d,%Y %H:%M')

        # check bookmarks
        with open(self.bookmark_path, 'r') as f:
            bookmarks = json.load(f)

        if title not in bookmarks:
            # write to bookmarks
            bookmarks[title] = (most_recent_chapters[0], most_recent_times[0])
            print(f"ADDED: {title}, {most_recent_chapters[0]}")
            self.news = True
        else:
            chap, recent_time = bookmarks['title']
            bookmark_date = datetime.strptime(recent_time, '%b %d,%Y %H:%M')
            if newest > bookmark_date:
                i = 0
                while i < len(most_recent_times):
                    if datetime.strptime(most_recent_times[i], '%b %d,%Y %H:%M') >= bookmark_date and most_recent_chapters[i] != chap:
                        print(f"NEW: {title}, {most_recent_chapters[i]}: {links[i]}")
                bookmarks[title] = (most_recent_chapters[0], newest)
                self.news = True
        
        if self.news:
            with open(self.bookmark_path, 'w') as f:
                json.dump(bookmarks, f,ensure_ascii=False)

    def closed(self, reason):
        if not self.news:
            print("No new manga now. :(")