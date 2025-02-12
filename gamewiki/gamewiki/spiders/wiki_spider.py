import scrapy

class WikiSpider(scrapy.Spider):
    name = "wiki_spider"
    allowed_domains = ["warframe.fandom.com"]  # Replace with actual domain
    start_urls = ["https://warframe.fandom.com/wiki/Local_Sitemap"]  # Starting point

    def parse(self, response):
        # Extract all links from the page
        for link in response.css("a::attr(href)").getall():
            if link.startswith("/wiki/") and ":" not in link:  # Avoid non-content pages
                full_url = response.urljoin(link)
                yield scrapy.Request(full_url, callback=self.parse_page)

    def parse_page(self, response):
        title = response.css("h1::text").get()
        content = " ".join(response.css("p::text").getall())

        yield {
            "url": response.url,
            "title": title,
            "content": content
        }
