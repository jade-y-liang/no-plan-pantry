#!/usr/bin/env python
# coding: utf-8

# In[1]:


#pip install transformers


# In[2]:


#get_ipython().system('pip install torch')


# In[3]:


import pandas as pd
import sqlite3
from recipe_query import query_recipes
from dash import Dash, html, dcc, ctx
from dash.dependencies import Input, Output, State
from dash import html, dcc, Input, Output, State, callback_context
import dash
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch


# ## set up `ingredients` table

# In[4]:


# Global database connection variable
recipes_db = None

def get_recipes_db():
    """Ensures a global database connection is available and returns it, setting it up if not already configured."""
    global recipes_db

    if recipes_db is not None: # if database is not empty
        return recipes_db
    else:
        # Connect to the database recipes_db.sqlite
        recipes_db = sqlite3.connect("recipes_db.sqlite", check_same_thread=False)

        # SQL command to create an `ingredients` table in the database if it does not exist
        cmd = '''
            CREATE TABLE IF NOT EXISTS ingredients (
            ingredient TEXT NOT NULL UNIQUE);
            '''
        cursor = recipes_db.cursor()
        cursor.execute(cmd)
        recipes_db.commit()  # Save changes
        cursor.close()  # closes cursor

    return recipes_db


# ## Add `recipes` table to database

# In[5]:


def setup_database():
    """ Imports data from CSV to SQL table using the global connection. """
    db = get_recipes_db()

    # Load data from a CSV file into a DataFrame
    recipes = pd.read_csv("https://raw.githubusercontent.com/jade-y-liang/pic16b-project/refs/heads/main/datasets/recipes_updated_new.csv")
    # Insert data from DataFrame to the SQL table, replacing if exists
    recipes.to_sql("recipes", db, if_exists="replace", index=False)

    # Verification query to check the tables in the database
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    cursor.close()

    return tables

# Call setup_database function and print the tables to verify
tables = setup_database()
print(tables)


# In[6]:


def insert_ingredient(ingredient):
    """
    Inserts a new ingredient into the database.
    Args:
        ingredient (str): The name of an ingredient.
    """

    # creating a cursor to our database

    db = get_recipes_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO ingredients (ingredient) VALUES (?)", (ingredient,))
        db.commit()
        return True  # Insertion was successful
    except sqlite3.IntegrityError:
        return False  # Insertion failed due to duplicate ingredient
    finally:
        cursor.close()

def fetch_ingredients():
    """ Fetches all ingredients from the database to display them """
    db = get_recipes_db()
    cursor = db.cursor()
    cursor.execute("SELECT ingredient FROM ingredients")
    ingredients = cursor.fetchall()
    cursor.close()
    return ingredients

def clear_ingredients():
    """Clears all ingredients from the database."""
    db = get_recipes_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM ingredients")
    db.commit()
    cursor.close()
    
def fetch_ingredients():
    """Fetches all ingredients from the database to display them."""
    db = get_recipes_db()
    cursor = db.cursor()
    cursor.execute("SELECT ingredient FROM ingredients")
    ingredients = cursor.fetchall()
    cursor.close()
    print(f"DEBUG: Current ingredients in database: {ingredients}")  # Debugging log
    return ingredients


# In[7]:


import dash
from dash import Dash, dcc, Output, Input, State, html, callback_context
import dash_bootstrap_components as dbc

#building the components
app = dash.Dash(__name__, external_stylesheets=[
    "https://fonts.googleapis.com/css2?family=Futura&display=swap", "https://fonts.googleapis.com/css2?family=Montserrat&display=swap"
]) #initialize our app

#button styling (for ingredients)
header_style= {
            'textAlign': 'center',
            'color': '#FFC107',
            'fontSize': '35px',
            'fontWeight': 'bold',
            'backgroundColor': '#7EBC89',
            'padding': '10px',
            'fontFamily': 'Futura',
            'borderRadius': '10px 10px 0 0',
            'width': '100%',
            'margin': '0'
        }
ingredients_section= {'fontFamily': 'Futura', 'color': '#FE5D26','marginBottom': '10px', 'textAlign': 'center', 'fontSize': '25px'}
button_style= {'margin': '5px', 'fontFamily': 'Futura','fontSize': '20px', 'fontWeight': 'bold','padding': '10px 10px', 
               'backgroundColor': '#FFB129', 'color': 'White', 'border': 'none', 'borderRadius': '8px', 'cursor': 'pointer', 'width': '150px', 'height': '50px'}

app.layout = html.Div([
    #title section
    html.Div([
        html.H1("No-Plan Pantry", style={
            'textAlign': 'center', 
            'color': '#7EBC89', 
            'fontFamily': 'Bebas Neue',
            'fontWeight': 'bold',
            'marginBottom': '20px',
            'fontSize': '100px'
        })
    ]),

    #description section
    html.Div([
        html.P(
            "Discover a new way to minimize food waste and unlock your inner chef. \n This application is designed to help you create delicious, easy-to-make recipes using leftover ingredients from your fridge. \n Simply input the items you have on hand, and let our app suggest creative meal ideas that are both tasty and resourceful. \n Whether you're looking to save time, reduce waste, or explore new recipes, this tool is here to inspire your cooking adventures. \n Give it a try and turn your leftovers into something delicious!",
            style={
                'textAlign': 'left',
                'fontSize': '18px',
                'fontFamily': 'Futura',
                'margin': '0',
                    'color': '#FE5D26'
            }
        )
    ], style={
        'backgroundColor': '#FAEDCA',
        'padding': '20px',
        'borderRadius': '10px',
        'margin': '20px auto',
        'maxWidth': '1100px'
    }),

    #ingredients section
    html.Div([
        html.H2("Ingredients:", style= header_style),
        html.Div([
            #vegetables column
            html.Div([
                html.H3("Vegetables:", style= ingredients_section ),
                html.Div([
                html.Button("Onion", id="onion-btn", style= button_style),
                html.Button("Corn", id="corn-btn", style= button_style),
                html.Button("Tomatoes", id="tomatoes-btn", style= button_style),
                html.Button("Potato", id="potato-btn", style= button_style),
                html.Button("Bell Pepper", id="bell pepper-btn", style= button_style),
                html.Button("Carrots", id="carrot-btn", style= button_style),
                html.Button("Pea", id="pea-btn", style= button_style),
                html.Button("Mushroom", id="mushroom-btn", style= button_style),
                html.Button("Bean", id="bean-btn", style= button_style),
                html.Button("Basil", id="basil-btn", style= button_style),
                html.Button("Cilantro", id="cilantro-btn", style= button_style),
                html.Button("Red Pepper", id="red pepper-btn", style= button_style),
                html.Button("Spinach", id="spinach-btn", style= button_style),
                html.Button("Jalapeno", id="jalapeno-btn", style= button_style),
                html.Button("Cabbage", id="cabbage-btn", style= button_style),
                html.Button("Zuchinni", id="zucchini-btn", style= button_style),
                html.Button("Cucumber", id="cucumber-btn", style= button_style),
                html.Button("Broccoli", id="broccoli-btn", style= button_style),
                html.Button("Lettuce", id="lettuce-btn", style= button_style),
            ], style={
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'space-evenly',  
                'alignItems': 'center',            
                'height': '100%',                  
                'maxHeight': 'none',             
                'overflowY': 'auto',               
                'padding': '10px',
            })
        ], style={
            'flex': '1',
            'textAlign': 'center',
            'padding': '10px'
        }),
            #proteins + grain column
            html.Div([
                #proteins section
                html.H3("Proteins:", style=ingredients_section),
                html.Div([
                html.Button("Egg", id="egg-btn", style= button_style),
                html.Button("Chicken", id="chicken-btn", style= button_style),
                html.Button("Beef", id="beef-btn", style= button_style),
                html.Button("Pork", id="pork-btn", style= button_style),
                html.Button("Bacon", id="bacon-btn", style= button_style),
                html.Button("Sausage", id="sausage-btn", style= button_style),
                html.Button("Shrimp", id="shrimp-btn", style= button_style),
                html.Button("Turkey", id="turkey-btn", style= button_style),
            ], style={
                'display': 'flex',
                'flexDirection': 'column',        
                'justifyContent': 'space-evenly',  
                'alignItems': 'center',            
                'padding': '10px'}),

                #grains section
                html.H3("Grains:", style=ingredients_section),
                html.Div([
                html.Button("Flour", id="flour-btn", style= button_style),
                html.Button("Bread", id="bread-btn", style= button_style),
                html.Button("Rice", id="rice-btn", style= button_style),
                html.Button("Oat", id="oat-btn", style= button_style),
                html.Button("Tortilla", id="tortilla-btn", style= button_style),
                html.Button("Wheat", id="wheat-btn", style= button_style),
            ], style={
                'display': 'flex',
                'flexDirection': 'column',        
                'justifyContent': 'space-evenly',
                'alignItems': 'center',            
                'padding': '10px'})
        ], style={
            'flex': '1',
            'textAlign': 'center',
            'padding': '10px',
            'borderLeft': '1px solid #A7C584',  #separator between columns
            'borderRight': '1px solid #A7C584'  #separator between columns
        }),
            
            #fruits + dairy column
            html.Div([
                #Fruits
                html.H3("Fruits:", style= ingredients_section),
                html.Div([
                html.Button("Apple", id="apple-btn", style= button_style),
                html.Button("Lime", id="lime-btn", style= button_style),
                html.Button("Orange", id="orange-btn", style= button_style),
                html.Button("Coconut", id="coconut-btn", style= button_style),
                html.Button("Strawberries", id="strawberries-btn", style= button_style),
                html.Button("Cherries", id="cherries-btn", style= button_style),
                html.Button("Avocado", id="avocado-btn", style= button_style),
                html.Button("Cranberries", id="cranberries-btn", style= button_style),
                html.Button("Banana", id="banana-btn", style= button_style),
                ],
                    style= {
                        'display': 'flex',
                        'flexDirection': 'column',          
                        'justifyContent': 'space-evenly',   
                        'alignItems': 'center',            
                        'padding': '10px',
                    }
                ),
        
                #dairy
                html.H3("Dairy:", style= ingredients_section),
                html.Div([
                html.Button("Milk", id="milk-btn", style=button_style),
                html.Button("Cheese", id="cheese-btn", style=button_style),
                html.Button("Yogurt", id="yogurt-btn", style=button_style),
                html.Button("Cream", id="cream-btn", style=button_style),
                    ],
                    style= {
                        'display': 'flex',
                        'flexDirection': 'column',
                        'justifyContent': 'space-evenly',
                        'alignItems': 'center',
                        'padding': '10px',
                    }
                )
            ], style={
                'flex': '1',
                'textAlign': 'center',
                'padding': '10px',
            }),
        ], style={
            'display': 'flex',
            'justifyContent': 'space-around',
            'alignItems': 'flex-start',
            'padding': '30px 20px',
        })
    ], style={
        'paddingTop': '10',
        'paddingBottom': '40px',
        'backgroundColor': '#FAEDCA',
        'borderRadius': '10px',
        'margin': '20px auto',
        'maxWidth': '1200px',
        'overflow': 'hidden',
    }),

        # Display Added Ingredients Section
    html.H3("Submitted Ingredients:", style={'textAlign': 'center'}),
    html.Div(id='ingredients-list', style={'fontFamily': 'Futura', 'marginTop': '20px', 'textAlign': 'center'}),  # Ensure this DIV is part of the layout


        # Section to display all submitted ingredients
    html.Ul(id="display-ingredients", style={'fontFamily': 'Futura', 'marginTop': '10px', 'textAlign': 'center', 'color':'white'}),


    #combining calories + time limit section
html.Div([
    #additional inputs section
    html.H2("Additional Inputs:", style=header_style),
    
    #calories subsection
    html.Div([
        html.H3("Calories:", style={
            'textAlign': 'center',
            'fontSize': '25px',
            'color': '#FE5D26',
            'fontFamily': 'Futura',
            'marginBottom': '10px',
            'marginTop': '30px'
        }),
        html.Div([
            dcc.Input(
                id='min-calories-input',
                type='number',
                placeholder='Min Calories',
                style={'fontFamily': 'Futura','width': '180px', 'marginBottom': '10px'}
            ),
            dcc.Input(
                id='max-calories-input',
                type='number',
                placeholder='Max Calories',
                style={'fontFamily': 'Futura','width': '180px', 'marginBottom': '20px'}
            ),
        ], style={
            'display': 'flex',
            'flexDirection': 'column',   
            'padding': '20px',
            'justifyContent': 'center',
            'alignItems': 'center',
        })
    ], style={
        'paddingBottom': '10px',
        'borderBottom': '1px solid #A7C584'
    }),
    
    #time limit subsection
    html.Div([
        html.H3("Time Limit (Cook & Prep Time in Minutes):", style={
            'textAlign': 'center',
            'fontSize': '25px',
            'color': '#FE5D26',
            'fontFamily': 'Futura',
            'marginBottom': '20px',
            'marginTop': '20px'
        }),
        html.Div([
            dcc.Slider(
                id='time-limit-slider',
                min=0,
                max=180,
                step=1,
                marks={i: f"{i}" for i in range(0, 181, 10)},
                value=60,
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], style={
            'padding': '20px 0',
            'fontFamily': 'Futura',
            'fontSize': '20px',
            'color': '#A7C584',
            'maxWidth': '800px',
            'width': '100%',
            'margin': '0 auto',
        }),
    ], style={
        'padding': '20px',
    }),
    
    #single submit button
    html.Div([
        html.Button("Submit", id="submit-btn", style={'margin': '10px auto', 
                                                      'fontFamily': 'Futura',
                                                      'fontWeight': 'bold',
                                                      'padding': '0', 
                                                      'backgroundColor': '#FFB129', 
                                                      'color': 'White', 
                                                      'border': 'none', 
                                                      'borderRadius': '8px', 
                                                      'cursor': 'pointer',
                                                      'width': '100px',  
                                                      'height': '40px',
                                                      'fontSize': '20px',
                                                      'textAlign': 'center',
                                                      'lineHeight': '40px',
                                                      'width': '150px',
                                                      'height': '50px'
                                                     }),
    ], style={
        'textAlign': 'center'
    })
], style={
    'paddingBottom': '20px',
    'backgroundColor': '#FAEDCA',
    'borderRadius': '10px',
    'marginBottom': '40px',
    'maxWidth': '1200px',
    'margin': '40px auto',
    'overflow': 'hidden'
}),
html.Div([
  
    dcc.ConfirmDialog(
        id='ingredients-dialog',
        message="Please select at least one ingredient before submitting.",
        displayed=False  # Initially hidden
    ),
]),

    html.Div([
    html.H2("Results:", style=header_style),
    html.Div([
        # Left Column (Feedback section)
        html.Div([
            html.H3("Traditional Recipe", style={'fontSize': '25px'}),
            html.P(id='name_1'),
            html.P(id='ingredients_1'),
            html.P(id='directions_1', style={'marginBottom': '50px'}),
            html.P(id='name_2'),
            html.P(id='ingredients_2'),
            html.P(id='directions_2', style={'marginBottom': '50px'}),
            html.P(id='name_3'),
            html.P(id='ingredients_3'),
            html.P(id='directions_3')
        ], style={
            'width': '45%',
            'fontFamily': 'Futura',
            'float': 'left',
            'padding': '10px',
            'marginRight': '5%'
        }),

        html.Div([
            html.H3("AI Generated Recipe", style={'fontSize': '25px'}),
            html.P(id='ai_directions')
        ], style={
            'width': '45%',
            'fontFamily': 'Futura',
            
            'float': 'left',
            'padding': '10px',
        }),
        
        # Clear floating div to avoid overlap
        html.Div(style={'clear': 'both'})
    ], id='results-content', style={
        'padding': '20px',
        'backgroundColor': '#FAEDCA',
        'borderRadius': '0 0 10px 10px'
    })
    ])
])


# @app.callback(
#     [Output('ingredients-list', 'children'),
#      Output('display-ingredients', 'children')],
#     [Input(f'{item}-btn', 'n_clicks') for item in [
#     "onion", "corn", "tomatoes", "potato", "bell pepper", "carrot", "pea", "mushroom",
#     "bean", "basil", "cilantro", "red pepper", "spinach", "jalapeno", "cabbage", "zucchini",
#     "cucumber", "broccoli", "lettuce", "egg", "chicken", "beef", "pork", "bacon", "sausage",
#     "shrimp", "turkey", "flour", "bread", "rice", "oat", "tortilla", "wheat", "apple", "lime",
#     "orange", "coconut", "strawberries", "cherries", "avocado", "cranberries", "banana", "milk",
#     "cheese", "yogurt", "cream"
# ]],
#     prevent_initial_call=True,
#     allow_duplicate = True
# )
# def update_ingredients_list(*args):
#     """ Updates ingredients table based on user input"""
#     triggered_id = ctx.triggered_id
#     ingredient = triggered_id.split('-')[0] if ctx.triggered_id else ''
    
#     # Attempt to insert the ingredient
#     success = insert_ingredient(ingredient)
    
#     # Fetch the updated list of ingredients to display
#     ingredients = fetch_ingredients()
#     list_items = [html.Li(ingredient[0]) for ingredient in ingredients]
    
#     # Create feedback message
#     feedback_message = f"Added: {ingredient}" if success else f"Duplicate not added: {ingredient}"
#     return feedback_message, list_items

# @app.callback(
#     [Output('name_1', 'children'),
#      Output('ingredients_1', 'children'),
#      Output('directions_1', 'children'),
#      Output('name_2', 'children'),
#      Output('ingredients_2', 'children'),
#      Output('directions_2', 'children'),
#      Output('name_3', 'children'),
#      Output('ingredients_3', 'children'),
#      Output('directions_3', 'children'),
#      Output('ingredients-dialog', 'displayed')],  # Add output for the dialog
#     [Input('submit-btn', 'n_clicks')],
#     [State('time-limit-slider', 'value'),
#      State('min-calories-input', 'value'),
#      State('max-calories-input', 'value'),
#      State('display-ingredients', 'children')],
#     prevent_initial_call=True
# )
# def update_recipes(n_clicks, time_limit, min_calories, max_calories, display_ingredients):
#     """ Retrieves recipes based on selected ingredients and filters"""
#     if n_clicks > 0:
#         # Check if ingredients are selected
#         if display_ingredients is None or len(display_ingredients) == 0:
#             # Trigger the popup if no ingredients are selected
#             return [None] * 9 + [True]  # No recipe data, just show the dialog
        
#         # Prepare ingredients list
#         ingredients = [ingredient['props']['children'] for ingredient in display_ingredients]
        
#         # Construct the query with dynamic conditions
#         query = "SELECT * FROM recipes WHERE total_time <= ?"
        
#         # Initialize parameters
#         params = [time_limit]
        
#         # Add calorie conditions only if valid
#         if min_calories is not None:
#             query += " AND calories_per_serving >= ?"
#             params.append(min_calories)
        
#         if max_calories is not None:
#             query += " AND calories_per_serving <= ?"
#             params.append(max_calories)
        
#         # Add ingredients conditions
#         if ingredients:
#             query += " AND ("
#             for ingredient in ingredients:
#                 query += "main_ingredients LIKE ? OR "
#             query = query.rstrip(" OR ") + ")"
#             params.extend([f"%{ingredient}%" for ingredient in ingredients])
        
#         # Connect to the SQLite database using sqlite3
#         try:
#             conn = sqlite3.connect('recipes_db.sqlite')  # Use SQLite connection
#             df = pd.read_sql_query(query, conn, params=params)
#             conn.close()  # Close connection after query
            
#         except Exception as e:
#             print(f"Error executing query: {e}")
#             return [None] * 9 + [False]  # Return empty results and hide the dialog
        
#         # Check if the dataframe is empty before accessing rows
#         if df.empty:
#             return [None] * 9 + [False]  # Return empty results and hide the dialog

#         # Extract top 3 recipes if available
#         recipe_1 = df.iloc[0] if len(df) > 0 else None
#         recipe_2 = df.iloc[1] if len(df) > 1 else None
#         recipe_3 = df.iloc[2] if len(df) > 2 else None
        
#         # Prepare output for the 3 recipes
#         name_1 = recipe_1['recipe_name'] if recipe_1 is not None else "No recipe found"
#         ingredients_1 = recipe_1['main_ingredients'] if recipe_1 is not None else "No ingredients"
#         directions_1 = recipe_1['direction_list'] if recipe_1 is not None else "No directions"
        
#         name_2 = recipe_2['recipe_name'] if recipe_2 is not None else "No recipe found"
#         ingredients_2 = recipe_2['main_ingredients'] if recipe_2 is not None else "No ingredients"
#         directions_2 = recipe_2['direction_list'] if recipe_2 is not None else "No directions"
        
#         name_3 = recipe_3['recipe_name'] if recipe_3 is not None else "No recipe found"
#         ingredients_3 = recipe_3['main_ingredients'] if recipe_3 is not None else "No ingredients"
#         directions_3 = recipe_3['direction_list'] if recipe_3 is not None else "No directions"
        
#         return name_1, ingredients_1, directions_1, name_2, ingredients_2, directions_2, name_3, ingredients_3, directions_3, False
    
#     return [None] * 9 + [False]





# In[8]:


@app.callback(
    [Output('name_1', 'children'),
     Output('ingredients_1', 'children'),
     Output('directions_1', 'children'),
     Output('name_2', 'children'),
     Output('ingredients_2', 'children'),
     Output('directions_2', 'children'),
     Output('name_3', 'children'),
     Output('ingredients_3', 'children'),
     Output('directions_3', 'children'),
     Output('ingredients-dialog', 'displayed'),
     Output('ingredients-list', 'children'),
     Output('display-ingredients', 'children'),
     Output('ai_directions', 'children')],  # AI-generated recipe
    [Input('submit-btn', 'n_clicks')] +
    [Input(f'{item}-btn', 'n_clicks') for item in [
        "onion", "corn", "tomatoes", "potato", "bell pepper", "carrot", "pea", "mushroom",
        "bean", "basil", "cilantro", "red pepper", "spinach", "jalapeno", "cabbage", "zucchini",
        "cucumber", "broccoli", "lettuce", "egg", "chicken", "beef", "pork", "bacon", "sausage",
        "shrimp", "turkey", "flour", "bread", "rice", "oat", "tortilla", "wheat", "apple", "lime",
        "orange", "coconut", "strawberries", "cherries", "avocado", "cranberries", "banana", "milk",
        "cheese", "yogurt", "cream"
    ]],
    [State('time-limit-slider', 'value'),
     State('min-calories-input', 'value'),
     State('max-calories-input', 'value'),
     State('display-ingredients', 'children')],
    prevent_initial_call=True
)
def update_recipes_and_ingredients(*args):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

    # If an item button is clicked
    if triggered_id and triggered_id != 'submit-btn':  # Item button clicked
        ingredient = triggered_id.split('-')[0]
        success = insert_ingredient(ingredient)
        ingredients = fetch_ingredients()
        list_items = [html.Li(ingredient[0]) for ingredient in ingredients]
        display_ingredients = [ingredient[0] for ingredient in ingredients]
        return [None] * 9 + [False, list_items, display_ingredients, ""]

    # If the submit button is clicked
    if triggered_id == 'submit-btn' and args[0] > 0:  # args[0] is n_clicks for submit-btn
        time_limit = args[-4] or 180  # Default to 180 if not set
        min_calories = args[-3] or 0  # Default to 0 if not set
        max_calories = args[-2] or 2000  # Default to 2000 if not set
        display_ingredients = args[-1]

        # Check if no ingredients are selected
        if not isinstance(display_ingredients, list) or len(display_ingredients) == 0:
            return [None] * 9 + [True, [], [], ""]  # Show dialog and reset outputs

        # Retrieve recipes using the query function
        try:
            df = query_recipes(
                "recipes_db.sqlite",
                ingredients=display_ingredients,
                time=time_limit,
                min_calories=min_calories,
                max_calories=max_calories
            )
        except Exception as e:
            return [None] * 9 + [False, [], [], ""]  # Clear lists and hide the dialog

        # Generate a fallback AI recipe
        from transformers import GPT2LMHeadModel, GPT2Tokenizer
        model_tuned = GPT2LMHeadModel.from_pretrained("./fine_tuned_recipe_model")
        tokenizer = GPT2Tokenizer.from_pretrained("./fine_tuned_recipe_model")

        prompt = f"Generate a recipe with the following ingredients: {', '.join(display_ingredients)}. Keep it under {time_limit} minutes."
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
        output_tuned = model_tuned.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=250,
            num_beams=5,
            no_repeat_ngram_size=2,
            early_stopping=True,
            eos_token_id=tokenizer.eos_token_id)

        generated_recipe = tokenizer.decode(output_tuned[0], skip_special_tokens=True)
        # Remove the prompt from the generated recipe
        if generated_recipe.startswith(prompt):
            generated_recipe = generated_recipe[len(prompt):].strip()

        # If recipes are found
        if not df.empty:
            recipe_1 = df.iloc[0] if len(df) > 0 else None
            recipe_2 = df.iloc[1] if len(df) > 1 else None
            recipe_3 = df.iloc[2] if len(df) > 2 else None

            def format_recipe(recipe, index):
                if recipe is None:
                    return (
                        f"Recipe {index}: No recipe found",
                        "Main Ingredients: No ingredients",
                        "Directions: No directions"
                    )
                name = f"Recipe {index}: {recipe.get('recipe_name', 'No recipe name')}"
                ingredients = recipe.get('main_ingredients', [])
                if isinstance(ingredients, list):
                    ingredients = f"Main Ingredients: {', '.join(ingredients)}"
                directions = f"Directions: {recipe.get('direction_list', 'No directions')}"
                return name, ingredients, directions

            name_1, ingredients_1, directions_1 = format_recipe(recipe_1, 1)
            name_2, ingredients_2, directions_2 = format_recipe(recipe_2, 2)
            name_3, ingredients_3, directions_3 = format_recipe(recipe_3, 3)

            # Clear ingredients after successful query
            clear_ingredients()
            return (
                name_1, ingredients_1, directions_1,
                name_2, ingredients_2, directions_2,
                name_3, ingredients_3, directions_3,
                False, [], [], generated_recipe
            )

        # If no recipes are found, return only the AI-generated recipe
        return (
            "Generated Recipe: AI", "Main Ingredients: AI-generated", generated_recipe,
            None, None, None,
            None, None, None,
            False, [], [], generated_recipe
        )

    # Default return
    return [None] * 9 + [False, [], [], ""]


# In[9]:


if __name__ == '__main__':
    app.run_server(debug=True)


# ## Getting Recommended Recipes Based on User Input

# In[10]:


query = "SELECT * FROM ingredients"

# Read the query results into a DataFrame
df = pd.read_sql_query(query, recipes_db)
ings = [df["ingredient"][i] for i in range(len(df))]
ings


# In[11]:


df = query_recipes("recipes_db.sqlite", 
                   ingredients=ings,
                   time = 180,
                   min_calories = 0, 
                   max_calories = 2000
                   )
df.head(3)


# In[ ]:




