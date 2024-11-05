import scrapy
from urllib.parse import urljoin

class PropertySpider(scrapy.Spider):
    name = 'property_spider'
    start_urls = ['https://www.realtor.com/realestateandhomes-search/90024']

    def parse(self, response):
        """
        Parse the initial search result page and return each property link
        """
        
        # Extract all property links
        property_links = response.css("div[data-testid='card-media'] a::attr(href)").getall()

        # Yield each link as an item
        for link in property_links:
            yield {
                'property_link': response.urljoin(link)
            #scrapy.Request(urljoin(base_url, link), callback = self.parse_detail_page)
            }
            
        # Find the "Next" button link and follow it if it exists
        next_page = response.css("a[aria-label="Next page"]::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    # def parse_detail_page(self, response):
