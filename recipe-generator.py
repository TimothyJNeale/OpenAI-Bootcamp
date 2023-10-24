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
    prompt = f"""Create a detailed recipe based on only the following ingredients:
    #
    # Ingredients:
    # {', '.join(ingredients)}
    #
    # Instructions:"""
    return prompt
