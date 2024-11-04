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
        hrefs = response.css('div[id^="property_id_"] a::attr(href)').getall()

        for href in hrefs:
            yield scrapy.Request(urljoin(base_url, href), callback = self.parse_detail_page)

