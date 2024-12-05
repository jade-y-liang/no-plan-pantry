#!/usr/bin/env python
# coding: utf-8

# In[427]:


import dash
from dash import Dash, dcc, Output, Input, html
import dash_bootstrap_components as dbc


# In[429]:


#building the components
app = dash.Dash(__name__, external_stylesheets=[
    "https://fonts.googleapis.com/css2?family=Chewy&display=swap", "https://fonts.googleapis.com/css2?family=Nunito&display=swap"
]) #initialize our app


# In[775]:


#button styling (for ingredients)
header_style= {
            'textAlign': 'center',
            'color': '#F2C078',
            'fontSize': '35px',
            'fontWeight': 'bold',
            'backgroundColor': '#7EBC89',
            'padding': '10px',
            'fontFamily': 'Chewy',
            'borderRadius': '10px 10px 0 0',
            'width': '100%',
            'margin': '0'
        }
ingredients_section= {'fontFamily': 'Nunito, sans-serif', 'color': '#FE5D26','marginBottom': '10px', 'textAlign': 'center', 'fontSize': '25px'}
button_style= {'margin': '5px', 'fontFamily': 'Chewy','padding': '10px 10px', 
               'backgroundColor': '#7EBC89', 'color': 'white', 'border': 'none', 'borderRadius': '8px', 'cursor': 'pointer' }

app.layout = html.Div([
    #title section
    html.Div([
        html.H1("No-Plan Pantry", style={
            'textAlign': 'center', 
            'color': '#7EBC89', 
            'fontFamily': 'Chewy',
            'marginBottom': '20px',
            'fontSize': '40px'
        })
    ]),

    #description section
    html.Div([
        html.P(
            "Discover a new way to minimize food waste and unlock your inner chef. This application is designed to help you create delicious, easy-to-make recipes using leftover ingredients from your fridge. Simply input the items you have on hand, and let our app suggest creative meal ideas that are both tasty and resourceful. Whether you're looking to save time, reduce waste, or explore new recipes, this tool is here to inspire your cooking adventures. Give it a try and turn your leftovers into something delicious!",
            style={
                'textAlign': 'center',
                'fontSize': '14px',
                'fontFamily': 'Nunito, sans-serif',
                'margin': '0',
                    'color': '#FE5D26'
            }
        )
    ], style={
        'backgroundColor': '#FAEDCA',
        'padding': '20px',
        'borderRadius': '10px',
        'margin': '20px auto',
        'maxWidth': '600px'
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
                html.Button("Potatoes", id="potatoes-btn", style= button_style),
                html.Button("Bell Peppers", id="bellpepper-btn", style= button_style),
                html.Button("Carrots", id="carrot-btn", style= button_style),
                html.Button("Peas", id="peas-btn", style= button_style),
                html.Button("Mushrooms", id="mushrooms-btn", style= button_style),
                html.Button("Beans", id="bean-btn", style= button_style),
                html.Button("Basil", id="basil-btn", style= button_style),
                html.Button("Cilantro", id="cilantro-btn", style= button_style),
                html.Button("Red Peppers", id="redpepper-btn", style= button_style),
                html.Button("Spinach", id="spinach-btn", style= button_style),
                html.Button("Jalapeños", id="jalapenos-btn", style= button_style),
                html.Button("Cabbage", id="cabbage-btn", style= button_style),
                html.Button("Zuchinni", id="zuchinni-btn", style= button_style),
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
                html.Button("Eggs", id="eggs-btn", style= button_style),
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

                # Grains Section
                html.H3("Grains:", style=ingredients_section),
                html.Div([
                html.Button("Flour", id="flour-btn", style= button_style),
                html.Button("Bread", id="bread-btn", style= button_style),
                html.Button("Rice", id="rice-btn", style= button_style),
                html.Button("Oats", id="oats-btn", style= button_style),
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
            
            # Fruits and Dairy Column
            html.Div([
                #Fruits
                html.H3("Fruits:", style= ingredients_section),
                html.Div([
                html.Button("Apple", id="apple-btn", style= button_style),
                html.Button("Lime", id="lime-btn", style= button_style),
                html.Button("Orange", id="orange-btn", style= button_style),
                html.Button("Coconut", id="coconut-btn", style= button_style),
                html.Button("Strawberry", id="strawberry-btn", style= button_style),
                html.Button("Cherry", id="cherry-btn", style= button_style),
                html.Button("Avocado", id="avocado-btn", style= button_style),
                html.Button("Cranberry", id="cranberry-btn", style= button_style),
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
        
                #Dairy
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
            'fontFamily': 'Nunito, sans-serif',
            'marginBottom': '10px',
            'marginTop': '30px'
        }),
        html.Div([
            dcc.Input(
                id='min-calories-input',
                type='number',
                placeholder='Min Calories',
                style={'width': '180px', 'marginBottom': '10px'}
            ),
            dcc.Input(
                id='max-calories-input',
                type='number',
                placeholder='Max Calories',
                style={'width': '180px', 'marginBottom': '20px'}
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
    
    # Time Limit subsection
    html.Div([
        html.H3("Time Limit (Cook & Prep Time in Minutes):", style={
            'textAlign': 'center',
            'fontSize': '25px',
            'color': '#FE5D26',
            'fontFamily': 'Nunito, sans-serif',
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
                value=30,
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], style={
            'padding': '20px 0',
            'fontFamily': 'Nunito, sans-serif',
            'fontSize': '20px',
            'color': '#A7C584',
            'maxWidth': '800px',
            'width': '100%',
            'margin': '0 auto',
        }),
    ], style={
        'padding': '20px',
    }),
    
    # Single Submit Button
    html.Div([
        html.Button("Submit", id="submit-btn", style={'margin': '10px auto', 
                                                      'fontFamily': 'Chewy',
                                                      'padding': '0', 
                                                      'backgroundColor': '#7EBC89', 
                                                      'color': 'white', 
                                                      'border': 'none', 
                                                      'borderRadius': '8px', 
                                                      'cursor': 'pointer',
                                                      'width': '100px',  
                                                      'height': '40px',
                                                      'fontSize': '20px',
                                                      'textAlign': 'center',
                                                      'lineHeight': '40px'
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

    #results section
    html.Div([
        html.H2("Results:", style=header_style),
        html.Div(id='results-content', style={
        'padding': '20px',
        'backgroundColor': '#FAEDCA',
        'borderRadius': '0 0 10px 10px'
        })
    ], style={
        'borderRadius': '10px',
        'marginBottom': '40px',
        'maxWidth': '1200px',
        'margin': '0 auto',  
        'overflow': 'hidden'
    })
    
])


# In[777]:


#running the app
if __name__== '__main__':
    app.run_server(port= 8054)

