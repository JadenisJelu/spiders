import scrapy
import json

class MangaSpider(scrapy.Spider):
    name = "manga"
    bookmark_path = '/Users/jadenjelu/projects/spiders/manga/manga/bookmarks.json'
    news = False

    def start_requests(self):
        urls = [
            'https://readmanganato.com/manga-ec981811',
            'https://readmanganato.com/manga-dr980474',
            'https://readmanganato.com/manga-ci980191',
            'https://readmanganato.com/manga-ml989546',
            'https://readmanganato.com/manga-dg980989',
            'https://readmanganato.com/manga-hu985229',
            'https://readmanganato.com/manga-lu989229',
            'https://readmanganato.com/manga-jo986949',
            'https://readmanganato.com/manga-iw985579',
            'https://readmanganato.com/manga-nb990510',
            'https://readmanganato.com/manga-ko987549',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.xpath('/html/body/div[1]/div[3]/div[1]/div[2]/div[2]/h1/text()').get()
        most_recent_chapters = response.xpath('/html/body/div[1]/div[3]/div[1]/div[3]/ul/li/a/text()').getall()
        links = response.xpath('/html/body/div[1]/div[3]/div[1]/div[3]/ul/li/a/@href').getall()

        # newest chapter
        num = int(most_recent_chapters[0].split(' ')[-1])

        # check bookmarks
        with open(self.bookmark_path, 'r') as f:
            bookmarks = json.load(f)

        if title not in bookmarks:
            # write to bookmarks
            bookmarks[title] = num
            print(f"ADDED: {title}, {most_recent_chapters[0]}")
            self.news = True
        else:
            if num > bookmarks[title]:
                for i in range(num - bookmarks[title]-1, -1,-1):
                    print(f"NEW: {title}, {most_recent_chapters[i]}: {links[i]}")
                bookmarks[title] = num
                self.news = True
        
        if self.news:
            with open(self.bookmark_path, 'w') as f:
                json.dump(bookmarks, f,ensure_ascii=False)

    def closed(self, reason):
        if not self.news:
            print("No new manga now. :(")