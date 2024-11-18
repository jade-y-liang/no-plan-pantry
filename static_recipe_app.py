#!/usr/bin/env python
# coding: utf-8

# In[41]:


from dash import Dash, dcc, Output, Input, html
import dash_bootstrap_components as dbc


# In[43]:


#building the components
app = Dash(__name__) #here, we are initializing our app


# In[121]:


#defining the layout
app.layout = html.Div([
    # Title
    html.H1("Easy Recipes!", style={'textAlign': 'center', 'color': 'pink'}),

    # Description
    html.P(
        "blah blah blah", style={'textAlign': 'center', 'fontSize': '18px'}
    ),

    # Ingredients Section
    html.Div([
        html.H2("Ingredients:", style={'textAlign': 'left', 'marginTop': '30px'}),

        # First row: Vegetables (left), Proteins (center), Fruits (right)
        html.Div([
            # Vegetables
            html.Div([
                html.H3("Vegetables"),
                html.Div([
                    html.Div([
                        html.Span("Lettuce", style={'marginRight': '10px'}),
                        html.Button("Add", id="lettuce-btn")
                    ]),
                    html.Div([
                        html.Span("Cabbage", style={'marginRight': '10px'}),
                        html.Button("Add", id="cabbage-btn")
                    ]),
                    html.Div([
                        html.Span("Cucumbers", style={'marginRight': '10px'}),
                        html.Button("Add", id="cucumbers-btn")
                    ]),
                ], style={'marginLeft': '20px'}),
            ], style={'flex': '1', 'textAlign': 'left'}),

            # Proteins
            html.Div([
                html.H3("Proteins"),
                html.Div([
                    html.Div([
                        html.Span("Chicken", style={'marginRight': '10px'}),
                        html.Button("Add", id="chicken-btn")
                    ]),
                    html.Div([
                        html.Span("Beef", style={'marginRight': '10px'}),
                        html.Button("Add", id="beef-btn")
                    ]),
                    html.Div([
                        html.Span("Tofu", style={'marginRight': '10px'}),
                        html.Button("Add", id="tofu-btn")
                    ]),
                ], style={'marginLeft': '20px'}),
            ], style={'flex': '1', 'textAlign': 'center'}),

            # Fruits
            html.Div([
                html.H3("Fruits"),
                html.Div([
                    html.Div([
                        html.Span("Apple", style={'marginRight': '10px'}),
                        html.Button("Add", id="apple-btn")
                    ]),
                    html.Div([
                        html.Span("Banana", style={'marginRight': '10px'}),
                        html.Button("Add", id="banana-btn")
                    ]),
                    html.Div([
                        html.Span("Grapes", style={'marginRight': '10px'}),
                        html.Button("Add", id="grape-btn")
                    ]),
                ], style={'marginLeft': '20px'}),
            ], style={'flex': '1', 'textAlign': 'right'}),
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '30px'}),

        # Second row: Grains (left), Dairy (center), Condiments (right)
        html.Div([
            # Grains
            html.Div([
                html.H3("Grains"),
                html.Div([
                    html.Div([
                        html.Span("White Rice", style={'marginRight': '10px'}),
                        html.Button("Add", id="white_rice-btn")
                    ]),
                    html.Div([
                        html.Span("Oats", style={'marginRight': '10px'}),
                        html.Button("Add", id="oats-btn")
                    ]),
                    html.Div([
                        html.Span("Barley", style={'marginRight': '10px'}),
                        html.Button("Add", id="barley-btn")
                    ]),
                ], style={'marginLeft': '20px'}),
            ], style={'flex': '1', 'textAlign': 'left'}),

            # Dairy
            html.Div([
                html.H3("Dairy"),
                html.Div([
                    html.Div([
                        html.Span("Milk", style={'marginRight': '10px'}),
                        html.Button("Add", id="milk-btn")
                    ]),
                    html.Div([
                        html.Span("Cheese", style={'marginRight': '10px'}),
                        html.Button("Add", id="cheese-btn")
                    ]),
                    html.Div([
                        html.Span("Yogurt", style={'marginRight': '10px'}),
                        html.Button("Add", id="yogurt-btn")
                    ]),
                ], style={'marginLeft': '20px'}),
            ], style={'flex': '1', 'textAlign': 'center'}),

            # Condiments
            html.Div([
                html.H3("Condiments"),
                html.Div([
                    html.Div([
                        html.Span("Ketchup", style={'marginRight': '10px'}),
                        html.Button("Add", id="ketchup-btn")
                    ]),
                    html.Div([
                        html.Span("Mustard", style={'marginRight': '10px'}),
                        html.Button("Add", id="mustard-btn")
                    ]),
                    html.Div([
                        html.Span("Mayo", style={'marginRight': '10px'}),
                        html.Button("Add", id="mayo-btn")
                    ]),
                ], style={'marginLeft': '20px'}),
            ], style={'flex': '1', 'textAlign': 'right'}),
        ], style={'display': 'flex', 'justifyContent': 'space-between'})
    ]),

    # Additional Ingredients
    html.Div([
        html.H2("Additional Ingredients:", style={'marginTop': '40px'}),
        html.Div([
            dcc.Input(
                id='new-ingredient-input', 
                type='text', 
                placeholder='Enter ingredient name', 
                style={'width': '300px', 'marginRight': '10px'}
            ),
            html.Button("Add Ingredient", id="add-ingredient-btn", style={
                'backgroundColor': 'pink', 
                'border': 'none', 
                'color': 'white',
                'padding': '5px 10px',
                'cursor': 'pointer'
            })
        ], style={'display': 'flex', 'alignItems': 'center', 'marginTop': '10px'})
    ]),

    # Time Limit Section
    # Time Limit Section
    html.Div([
        html.H2("Time Limit (Cook & Prep Time):", style={'marginTop': '40px'}),
        dcc.Slider(
            id='time-limit-slider',
            min=0,
            max=60,
            step=1,
            marks={i: f"{i} min" for i in range(0, 61, 10)},  # Add marks at 10-minute intervals
            value=30,  # Default value
            tooltip={"placement": "bottom", "always_visible": True}
        ),
        html.Button("Submit", id="submit-btn", style={
            'marginTop': '20px',
            'backgroundColor': 'pink', 
            'color': 'white',
            'border': 'none',
            'padding': '10px 20px',
            'fontSize': '16px',
            'cursor': 'pointer',
            'display': 'block',
            'marginLeft': 'auto',
            'marginRight': 'auto'
        }),
    ], style={'marginTop': '20px', 'marginBottom': '40px'}),

    # Results Section
    html.Div([
        html.H2("Results:", style={'marginTop': '40px', 'textAlign': 'center'}),
        html.Div([
            # Matched Recipes
            html.Div([
                html.H3("Matched Recipes"),
                html.Ul([
                    html.Li("Chicken Nuggets"),
                    html.Li("Chicken Salad"),
                    html.Li("Chicken Noodle Soup"),
                ]),
            ], style={'flex': '1', 'textAlign': 'left', 'marginLeft': '20px'}),

            # AI-Generated Recipes
            html.Div([
                html.H3("AI-Generated Recipes"),
                html.Ul([
                    html.Li("Chicken Pho"),
                    html.Li("Fried Chicken"),
                    html.Li("Chicken Fried Rice"),
                ], style={'marginLeft': '0'})  # Ensure bullet points align with the header
            ]),
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop': '30px'})
    ])
])


# In[123]:


#running the app
if __name__== '__main__':
    app.run_server(port= 8051)

