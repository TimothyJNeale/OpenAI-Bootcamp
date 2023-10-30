import openai
import os

from git import Repo

from pathlib import Path
WORKING_PATH = "/Users/sealislandmedia/Desktop/TimothyJNeale.github.io"

PATH_TO_BLOG_REPO = Path(os.path.join(WORKING_PATH, ".git"))
PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent

PATH_TO_CONTENT = PATH_TO_BLOG/"content"
PATH_TO_CONTENT.mkdir(exist_ok=True, parents=True)

# load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()


def updae_blog(commit_message='Update blog'):
    repo = Repo(PATH_TO_BLOG_REPO)

    repo.git.add(all=True)
    repo.index.commit(commit_message)

    origin = repo.remote(name='origin')
    origin.push()

random_text_string = "werwerwerwerwerwerwefdkdvjdni8bbc"

# Write random text string to index.html
with open(PATH_TO_BLOG/"index.html", "w") as f:
    f.write(random_text_string)

# Update blog
updae_blog()



# get api key from environment variable
api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = api_key