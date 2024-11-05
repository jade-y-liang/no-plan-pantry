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
        property_links = set(response.css('div[id^="property_id_"] a::attr(href)').getall())

        # Yield each link as an item
        for link in property_links:
            yield { #'property_link': response.urljoin(link)
            scrapy.Request(urljoin(base_url, link), callback = self.parse_detail_page)}
            
        # Find the "Next" button link and follow it if it exists
        next_page = response.css('a.next-link::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_detail_page(self, response):
        """
        Parse the detials of each property
        """
        # Extract the information
        price = response.css('span.base__StyledType-rui__sc-108xfm0-0.mQZci::text').getall()[0]
        address = response.css('h1.sc-79f365fd-3.bUJjRW::text').get()
        beds = response.css('li[data-testid="property-meta-beds"] span::text').get()
        baths = response.css('li[data-testid="property-meta-baths"] span::text').get()
        sqft = response.css('li[data-testid="property-meta-sqft"] span::text').getall()[0]
        lot_size =  response.css('span[data-testid="meta-value"]::text').getall()[3]
        
        # Yield each item as a dictionary
        yield {
            'price': price,
            'address': address,
            'beds': beds,
            'baths': baths,
            'sqft': sqft,
            'lot_size': lot_size,
        }
