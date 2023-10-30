import openai
import os
import shutil

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

def create_post(title, content, cover_image=None):
    cover_image = Path(cover_image)

    files = len(list(PATH_TO_CONTENT.glob("*.html")))
    new_title = f"{files+1}.html"
    path_to_new_post = PATH_TO_CONTENT/new_title

    shutil.copy(cover_image, PATH_TO_CONTENT)

    if not os.path.exists(path_to_new_post):
        with open(path_to_new_post, "w") as f:
            f.write('<DOCTYPE html>\n')
            f.write('<html>\n')
            f.write('<head>\n')
            f.write('<meta charset="utf-8">\n')
            f.write('<meta name="viewport" content="width=device-width, initial-scale=1">\n')
            f.write(f'<title>{title}</title>\n')
            f.write('</head>\n')
            f.write('<body>\n')
            f.write(f"<img src='{cover_image.name}' alt='Cover Image'> <br /> \n")
            f.write(f'<h1>{title}</h1>\n')
            f.write(content.replace('\n', '<br /> \n'))
            f.write('</body>\n')
            f.write('</html>\n')

            print(f"Created new post: {path_to_new_post}")
            return path_to_new_post
        
    else:
        raise FileExistsError("File already exists")


path_to_new_post = create_post("Test Post", "This is a test post", cover_image="dev/Engineering.png")



# get api key from environment variable
api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = api_key