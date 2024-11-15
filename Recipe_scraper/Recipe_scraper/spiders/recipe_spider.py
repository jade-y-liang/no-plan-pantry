import scrapy

class RecipeSpider(scrapy.Spider):
    name = 'recipe_spider'
    start_urls = ['https://www.allrecipes.com/recipes-a-z-6735880']

    def parse(self, response):
        """
        Parse the overview page and return each category link
        """
        
        # Extract all category links and their names
        categories = response.css('div.mntl-alphabetical-list__group a')
        for category in categories:
            link = category.css('::attr(href)').get()
            category_name = category.css('::text').get()  # Extract category name
            
            # Pass category_name to the next request using meta
            yield scrapy.Request(
                url=link, 
                callback=self.parse_menu_page, 
                meta={'category_name': category_name} # to later output category name for each recipe
            )
            
    def parse_menu_page(self, response):
        """
        Parse each category page and follow each recipe link.
        """
        
        # Access category name from response.meta
        category_name = response.meta['category_name']

        # Extract each recipe link on the category page
        three_recommended_recipes = response.css("div[id='mntl-three-post__inner_1-0'] a::attr(href)").getall()
        all_recipes = response.css("div[id='mntl-taxonomysc-article-list-group_1-0'] a::attr(href)").getall()
        recipe_links = three_recommended_recipes + all_recipes

        # Follow each recipe link to get recipe details
        for recipe_link in recipe_links:
            yield scrapy.Request(url=recipe_link, 
                                 callback=self.parse_detail_page,
                                 meta={'category_name': category_name} # to later output category name for each recipe
                                 )
    
    
    def parse_detail_page(self, response):
        """Extract recipe name, prep time, cook time, total time, ingredients, directions, and 
            nutrition facts (per serving) from each recipe page
        """
        # Access category name from response.meta
        category_name = response.meta['category_name']

        recipe_name = response.css("h1::text").get()

        # Extract recipe rating (will yield None if no ratings exist)
        recipe_rating = response.css("div[id='mm-recipes-review-bar__rating_1-0']::text").get()
        
        # Extract the time information individually and handle missing values
        # (missing values will return None)
        prep_time = response.xpath("//div[div[text()='Prep Time:']]/div[@class='mm-recipes-details__value']/text()").get()
        cook_time = response.xpath("//div[div[text()='Cook Time:']]/div[@class='mm-recipes-details__value']/text()").get()
        total_time = response.xpath("//div[div[text()='Total Time:']]/div[@class='mm-recipes-details__value']/text()").get()
        servings = response.xpath("//div[div[text()='Servings:']]/div[@class='mm-recipes-details__value']/text()").get()

        # this gives list of ingredients AND amount of ingredients (need manipulation)
        # raw_ingredients_list = response.css("ul.mm-recipes-structured-ingredients__list li.mm-recipes-structured-ingredients__list-item ::text").getall()
        ingredients_list = response.css('span[data-ingredient-name="true"]::text').getall()
        direction_list = response.css('ol[class="comp mntl-sc-block mntl-sc-block-startgroup mntl-sc-block-group--OL"] p::text').getall()

        # Extract nutrition facts with handling for missing values
        # (missing values will return None)
        values = response.css("tbody.mm-recipes-nutrition-facts-label__table-body.text-utility-300 td::text").getall()

        nutrition_data = {}
        # Define the labels we are interested in and use XPath to find each one
        nutrients = {
            'Total Fat': response.xpath("normalize-space(//tr[td/span[contains(text(), 'Total Fat')]]/td[1]/span/following-sibling::text()[1])").get(),
            'Saturated Fat': response.xpath("normalize-space(//tr[td/span[contains(text(), 'Saturated Fat')]]/td[1]/span/following-sibling::text()[1])").get(),
            'Cholesterol': response.xpath("normalize-space(//tr[td/span[contains(text(), 'Cholesterol')]]/td[1]/span/following-sibling::text()[1])").get(),
            'Sodium': response.xpath("normalize-space(//tr[td/span[contains(text(), 'Sodium')]]/td[1]/span/following-sibling::text()[1])").get(),
            'Total Carbohydrate': response.xpath("normalize-space(//tr[td/span[contains(text(), 'Total Carbohydrate')]]/td[1]/span/following-sibling::text()[1])").get(),
            'Dietary Fiber': response.xpath("normalize-space(//tr[td/span[contains(text(), 'Dietary Fiber')]]/td[1]/span/following-sibling::text()[1])").get(),
            'Total Sugars': response.xpath("normalize-space(//tr[td/span[contains(text(), 'Total Sugars')]]/td[1]/span/following-sibling::text()[1])").get(),
            'Protein': response.xpath("normalize-space(//tr[td/span[contains(text(), 'Protein')]]/td[1]/span/following-sibling::text()[1])").get(),
            'Vitamin C': response.xpath("normalize-space(//tr[td/span[contains(text(), 'Vitamin C')]]/td[1]/span/following-sibling::text()[1])").get(),
            'Calcium': response.xpath("normalize-space(//tr[td/span[contains(text(), 'Calcium')]]/td[1]/span/following-sibling::text()[1])").get(),
            'Iron': response.xpath("normalize-space(//tr[td/span[contains(text(), 'Iron')]]/td[1]/span/following-sibling::text()[1])").get(),
            'Potassium': response.xpath("normalize-space(//tr[td/span[contains(text(), 'Potassium')]]/td[1]/span/following-sibling::text()[1])").get(),
        }

        # Clean the extracted values (remove extra whitespace) and add them to nutrition_data
        for nutrient, value in nutrients.items():
            nutrition_data[nutrient] = value.strip() if value else None

        calories = response.css("tr.mm-recipes-nutrition-facts-label__calories th.mm-recipes-nutrition-facts-label__table-head-subtitle span + span::text").get()
        total_fat = nutrition_data.get("Total Fat")
        saturated_fat = nutrition_data.get("Saturated Fat")
        sodium_mg = nutrition_data.get("Sodium")
        grams_of_protein = nutrition_data.get("Protein")
        grams_of_carbs = nutrition_data.get("Total Carbohydrate")
        fiber = nutrition_data.get("Dietary Fiber")
        sugar = nutrition_data.get("Total Sugars")
        cholesterol_mg = nutrition_data.get("Cholesterol")
        vitamin_c_mg = nutrition_data.get("Vitamin C")
        calcium_mg = nutrition_data.get("Calcium")
        iron_mg = nutrition_data.get("Iron")
        potassium_mg = nutrition_data.get("Potassium")

        yield {'recipe_name' : recipe_name,
               'category_name' : category_name,
               'rating' : recipe_rating,
               'prep_time' : prep_time,
               'cook_time' : cook_time,
               'total_time' : total_time,
               'num_servings_per_recipe' : servings,
               'ingredients_list' : ingredients_list,
               'direction_list': direction_list,
               'calories_per_serving' : calories,
               'total_fat (g)' : total_fat,
               'saturated_fat (g)' : saturated_fat,
               "sodium (mg)" : sodium_mg,
               'protein (g)' : grams_of_protein,
               'carbs (g)' : grams_of_carbs,
               'fiber (g)' : fiber,
               'sugar (g)' : sugar,
               'cholesterol (mg)' :cholesterol_mg,
               'vitamin_c (mg)' :vitamin_c_mg,
               'calcium (mg)' : calcium_mg,
               'iron (mg)' : iron_mg,
               'potassium (mg)' : potassium_mg,
               'recipe_link' : response.url
        }

    
