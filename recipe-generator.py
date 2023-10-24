''' An application to generate a recipe and an image from a list of ingredients.
    THis uses calls to open API LLMs for recipie and image of the dish.'''

import openai
from dotenv import load_dotenv
import os

# load environment variables from .env file
load_dotenv()

# get api key from environment variable
openai.api_key = os.environ["OPENAI_API_KEY"]

# Create the prompt for the recipe
def create_recipe_prompt(ingredients):
    list_of_ingredients = '\n    #      '.join(ingredients)
    prompt = f"""
    # Create a detailed recipe based only on the following listed ingredients.
    # Additionally, assign a title starting with 'Recipe Title' to the recipe.
    #
    # Recipe Title:
    #
    # Ingredients:
    #      {list_of_ingredients}
    #
    # Instructions:"""
    return prompt

prompt = create_recipe_prompt(['chicken', 'rice', 'broccoli'])
print

response = openai.Completion.create(engine="text-davinci-003",
                                    prompt=prompt,
                                    max_tokens=256,
                                    temperature=0.8)

print(response['choices'][0]['text'])