import openai
from dotenv import load_dotenv
import os
import praw

# load environment variables from .env file
load_dotenv()

reddit = praw.Reddit(client_id=os.environ["REDDIT_CLIENT_ID"],
                     client_secret=os.environ["REDDIT_CLIENT_SECRET"],
                     user_agent=os.environ["REDDIT_USER_AGENT"]
                     )

for submision in reddit.subreddit("finance").hot(limit=5):
    print(submision.title)
                                    
# get api key from environment variable
api_key = os.environ["OPENAI_API_KEY"]
print(api_key)

openai.api_key = api_key
