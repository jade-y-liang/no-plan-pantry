import sqlite3
import pandas as pd

def clean_main_ingredients(ingredient_string):
    """ Converts main_ingredients string into a list of ingredients"""
    return ingredient_string.split(", ")

def clean_ingredients(str):
    return str.replace("[", "").replace("]", "").replace("'", "")

def contains_ings(ings1, ings2):
    """Checks if all items in ings1 are in ings2."""
    return all(ing in ings2 for ing in ings1)


# this function assumes `ingredients_list` in `recipes` are lists
# and total_time in `recipes` are integers that represent minutes
# (not the case in raw dataset)

def query_recipes(db_file, ingredients = [], time = float('inf'),
                  min_calories = 0, max_calories = float('inf')):
    """ returns a list of recipes that contains given ingredients, is within available 
    time, and each serving of recipe has calories within the range [min_calories, max_calories]

    Args:
        db_file (string): file name for the database. 
        ingredients (list, optional): a list of main ingredients (string). Defaults to [].
        time (float, optional): maximum minutes that user has available to cook. Defaults to inf.
        min_calories (float, optional): minimum calories that user wants per serving. Defaults to 0.
        max_calories (float, optional): maximum calories that user wants per serving. Defaults to inf.

    Returns:
        df (Pandas dataframe): a dataframe of recipes that match the given inputs
    """

    # replace infinity with a large number for SQLite compatibility
    max_time = time if time != float('inf') else 1e9
    max_cal = max_calories if max_calories != float('inf') else 1e9

    with sqlite3.connect(db_file) as conn:
        # fetch all recipes that match calorie and time constraints
        query = f"""
            SELECT * FROM recipes
            WHERE calories_per_serving >= {min_calories}
            AND calories_per_serving <= {max_cal}
            AND total_time <= {max_time}
        """
        
        df = pd.read_sql_query(query, conn)
        

    if ingredients != []:
        # convert main_ingredients string into lists
        df["main_ingredients"] = df["main_ingredients"].apply(clean_main_ingredients) 

        # filter out recipes where all main_ingredients are in ingredients
        df = df[[contains_ings(df.iloc[i, df.columns.get_loc('main_ingredients')], ingredients) for i in range(len(df))]]    

        # sort df to display best matched recipes (i.e. recipes that contains most/all ingredients from inputted ingredients)
        df = df.sort_values(by = 'main_ing_len', ascending=False)
       
    return df
