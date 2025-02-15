# No-Plan Pantry
## Overview:
Our project, “No-Plan Pantry”, aims to minimize food waste and inspire creativity in the kitchen by developing a web-application which generates recipes based on user-inputted ingredients. Using web scraping, recipes are collected from allrecipes.com and cleaned to ensure data quality. Advanced machine learning models, such as GPT-2 and BERT, are further employed to generate AI-based recipes and predict cooking times using textual recipe instructions. The application integrates these features with a user-friendly interface developed using Dash.

Data cleaning plays a critical role in standardizing recipe information, such as unifying time units, extracting key ingredients, and estimating missing cooking times. This step ensures the dataset is well-structured for machine learning models, enabling accurate recipe recommendations and cooking time predictions. The app’s interactivity allows users to select ingredients, set time or calorie preferences, and view both AI-generated and sourced recipes in an organized layout.

Overall, the No-Plan Pantry project combines data science, natural language processing, and intuitive design to create an innovative tool that empowers users to cook creatively while reducing food waste.

## How to Use the Web App:

First, please clone this resposity to your computer. You can do so by running the following code on your terminal.
```
git clone https://github.com/jade-y-liang/no-plan-pantry.git
```

_(Note: This method does **not** correctly download the "model.safetensors" file located in "Web_Application/fine_tuned_recipe_model" to your computer.)_

After cloning this repository, please navigate to the "fine_tuned_recipe_model" folder inside the "Web_Application" directory on this page.

Manually download the "model.safetensors" file from the "fine_tuned_recipe_model" folder, and replace the existing file in your cloned repository. The correct "model.safetensors" file should be **497.8MB** in size.

Then run the following code on your terminal.
```
cd no-plan-pantry
python Web_Application/webapp.py
```

The terminal window will then display a message like "Dash is running on http://". You can simply copy and paste the link shown on your terminal window to visit the web page. After you're done with the web app, simply click ctrl+C on your terminal window to exit the web app. 
