import scrapy

class PropertySpider(scrapy.Spider):
    name = 'recipe_spider'
    start_urls = ['https://www.allrecipes.com/recipes-a-z-6735880']

    def parse(self, response):
        """
        Parse the overview page and return each category link
        """
        
        # Extract all property links
        category_links = response.css('div.mntl-alphabetical-list__group a::attr(href)').getall()

        # Yield each link as an item
        for link in category_links:
            yield { 'category_link': link}
            #scrapy.Request(link, callback = self.parse_menu_page)}
            
    #def parse_menu_page(self, response):
    
    
    #def parse_detail_page(self, response):

    
