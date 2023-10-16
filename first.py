import openai
from dotenv import load_dotenv
import os

# load environment variables from .env file
load_dotenv()

# get api key from environment variable
api_key = os.environ["OPENAI_API_KEY"]
print(api_key)

openai.api_key = api_key
print(openai.Engine.list())
