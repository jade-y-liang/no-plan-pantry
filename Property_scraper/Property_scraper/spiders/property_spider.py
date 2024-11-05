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
        property_links = response.css('div[id^="property_id_"] a::attr(href)').getall()

        # Yield each link as an item
        for link in property_links:
            yield {
                'property_link': response.urljoin(link)
            }       