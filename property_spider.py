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
        for link in linkss:
            yield scrapy.Request(urljoin(base_url, link), callback = self.parse_detail_page)
            
        # Find the "Next" button link and follow it if it exists
        next_page = response.css('a.next-link::attr(href)').get()
        if next_page:
            # If the next page link is found, follow it and call parse() again
            yield response.follow(next_page, self.parse)

