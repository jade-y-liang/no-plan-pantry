#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import scrapy
from urllib.parse import urljoin

class PropertySpider(scrapy.Spider):
    name = 'property_spider'
    start_urls = ['https://www.realtor.com/realestateandhomes-search/Los-Angeles_CA'] 

    def parse(self, response):
        """
        Retrieve the link for each listed property
        """
        # Define a base URL
        base_url = 'https://www.realtor.com/'

        # Use CSS selectors to select links to page with details
        links = response.css('div[id^="property_id_"] a::attr(href)').getall()
        for link in links:
            yield scrapy.Request(urljoin(base_url, link), callback = self.parse_detail_page)
            
        # Find the "Next" button link and follow it if it exists
        next_page = response.css('a[aria-label="Next page"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
        # Generate a list of integers from 2 to 206
#        page_numbers = list(range(2, 207))
#        # Format the page numbers into the specified URL to follow
#        next_page = [f"https://www.realtor.com/realestateandhomes-search/Los-Angeles_CA/pg-{page_number}" for page_number in page_numbers]
#
#        for url in next_page:
#            # If the next page link is found, follow it and call parse() again
#            yield response.follow(url, self.parse)
    def parse_detail_page(self, response):
        price = response.css('span.base__StyledType-rui__sc-108xfm0-0.mQZci::text').getall()[0]
        address = response.css('h1.sc-79f365fd-3.bUJjRW::text').get()
        beds = response.css('li[data-testid="property-meta-beds"] span::text').get()
        baths = response.css('li[data-testid="property-meta-baths"] span::text').get()
        sqft = response.css('li[data-testid="property-meta-sqft"] span::text').getall()[0]
        lot_size =  response.css('span[data-testid="meta-value"]::text').getall()[3]

        yield {
            'price': price,
            'address': address,
            'beds': beds,
            'baths': baths,
            'sqft': sqft,
            'lot_size': lot_size,
        }
