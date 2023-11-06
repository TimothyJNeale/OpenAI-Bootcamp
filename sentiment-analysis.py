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

subreddit_stocks = reddit.subreddit("stocks")
print(subreddit_stocks.display_name)
print(subreddit_stocks.title)
#print(subreddit_stocks.description)
print(subreddit_stocks.accounts_active)

for posts in subreddit_stocks.hot(limit=5):    
    print(posts.title)
    submission = reddit.submission(id=posts.id)
    # print top 2 comments per submission
    counter = 0
    for top_level_comment in submission.comments:
        if top_level_comment != '[deleted]':
            print(top_level_comment.body)
            counter += 1
            if counter == 2:
                break
                                    
# # get api key from environment variable
# api_key = os.environ["OPENAI_API_KEY"]
# print(api_key)

# openai.api_key = api_key
