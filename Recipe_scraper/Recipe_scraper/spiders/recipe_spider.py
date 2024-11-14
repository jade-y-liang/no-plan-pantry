import scrapy

class RecipeSpider(scrapy.Spider):
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
            
    def parse_menu_page(self, response):
        """
        Parse each category page and follow each recipe link.
        """
        
        # Extract each recipe link on the category page
        three_recommended_recipes = response.css("div[id='mntl-three-post__inner_1-0'] a::attr(href)").getall()
        all_recipes = response.css("div[id='mntl-taxonomysc-article-list-group_1-0'] a::attr(href)").getall()
        recipe_link = three_recommended_recipes + all_recipes

        # Follow each recipe link to get recipe details
        for recipe_link in recipe_links:
            yield scrapy.Request(url=recipe_link, callback=self.parse_detail_page)
    
    
    def parse_detail_page(self, response):
        """Extract recipe name, prep time, cook time, total time, ingredients, directions, and 
            nutrition facts (per serving) from each recipe page
        """

        recipe_name = response.css("h1::text").get()
        prep_time = response.css("div[class='comp mm-recipes-details'] div.mm-recipes-details__value::text").getall()[0]
        cook_time = response.css("div[class='comp mm-recipes-details'] div.mm-recipes-details__value::text").getall()[1]
        total_time = response.css("div[class='comp mm-recipes-details'] div.mm-recipes-details__value::text").getall()[2]
        ingredients_list = response.css('span[data-ingredient-name="true"]::text').getall()
        direction_list = response.css('ol[class="comp mntl-sc-block mntl-sc-block-startgroup mntl-sc-block-group--OL"] p::text').getall()
        calories = response.css('td[class="mm-recipes-nutrition-facts-summary__table-cell text-body-100-prominent"]::text').getall()[0]
        grams_of_fat = response.css('td[class="mm-recipes-nutrition-facts-summary__table-cell text-body-100-prominent"]::text').getall()[1]
        grams_of_carbs = response.css('td[class="mm-recipes-nutrition-facts-summary__table-cell text-body-100-prominent"]::text').getall(2)
        grams_of_protein = response.css('td[class="mm-recipes-nutrition-facts-summary__table-cell text-body-100-prominent"]::text').getall(3)

        yield {'recipe_name' : recipe_name,
               'prep_time' : prep_time,
               'cook_time' : cook_time,
               'total_time' : total_time,
               'ingredients_list' : ingredients_list,
               'direction_list': direction_list,
               'calories' : calories,
               'grams_of_fat' : grams_of_fat,
               'grams_of_carbs' : grams_of_carbs,
               'grams_of_protein' : grams_of_protein
        }

    
