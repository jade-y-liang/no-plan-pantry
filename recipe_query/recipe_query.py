# alternatively, use this to check if user has all required ingredients
def contains_all_ingredients(recipe_ings, user_ings):
    for user_ing in user_ings:
        if not any(user_ing in recipe_ing for recipe_ing in recipe_ings):
            return False
    return True

import sqlite3
import sqlite3
import pandas as pd

# this function assumes `ingredients_list` in `recipes` are lists
# and total_time in `recipes` are integers that represent minutes
# (not the case in raw dataset)

def query_recipes(db_file, ingredients = [], time = float('inf'),
                  min_calories = 0, max_calories = float('inf')):
    """ returns a list of recipes that contains given ingredients, is within available 
    time, and each serving of recipe has calories within the range [min_calories, max_calories]

    Args:
        db_file (string): file name for the database. 
        ingredients (list, optional): a list of ingredients (string). Defaults to [].
        time (float, optional): maximum minutes that user has available to cook. Defaults to inf.
        min_calories (float, optional): minimum calories that user wants per serving. Defaults to 0.
        max_calories (float, optional): maximum calories that user wants per serving. Defaults to inf.

    Returns:
        df (Pandas dataframe): a dataframe of recipes that match the given inputs
    """

    # Replace infinity with a large number for SQLite compatibility
    max_time = time if time != float('inf') else 1e9
    max_cal = max_calories if max_calories != float('inf') else 1e9

    with sqlite3.connect(db_file) as conn:
        # Fetch all recipes that match calorie and time constraints
        query = f"""
            SELECT * FROM recipes
            WHERE calories_per_serving >= {min_calories}
            AND calories_per_serving <= {max_cal}
            AND total_time <= {max_time}
        """
        df = pd.read_sql_query(query, conn)
        
    # Filter the dataframe for recipes that contain all the required ingredients
    df = df[df['ingredients_list'].apply(lambda x: contains_all_ingredients(x.split(", "), ingredients))]
        
    return df
