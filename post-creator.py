import openai
import os
import shutil

from dotenv import load_dotenv
from git import Repo
from bs4 import BeautifulSoup as Soup
from pathlib import Path

WORKING_PATH = "/Users/sealislandmedia/Desktop/TimothyJNeale.github.io"
PATH_TO_BLOG_REPO = Path(os.path.join(WORKING_PATH, ".git"))
PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent

PATH_TO_CONTENT = PATH_TO_BLOG/"content"
PATH_TO_CONTENT.mkdir(exist_ok=True, parents=True)


 ############# Helper functions #############
def update_blog(commit_message='Update blog'):
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



# Check for duplicate links
def check_for_duplicate_links(path_to_new_content, links):
    urls = [str(link.get("href")) for link in links]
    content_path = str(Path(*path_to_new_content.parts[-2:]))
    return content_path in urls



def write_to_index(path_to_new_content):
    with open(PATH_TO_BLOG/"index.html") as index:
        soup = Soup(index.read())
    
    links = soup.find_all("a")
    last_link = links[-1]

    if check_for_duplicate_links(path_to_new_content, links):
        raise ValueError("Link already exists in index")
    
    link_to_new_blog = soup.new_tag("a", href=Path(*path_to_new_content.parts[-2:]))
    link_to_new_blog.string = path_to_new_content.name.split(".")[0]
    last_link.insert_after(link_to_new_blog)

    with open(PATH_TO_BLOG/"index.html", "w") as f:
        f.write(str(soup.prettify(formatter="html5")))

############# Execution code starts here #############


path_to_new_post = create_post("Test Post", "This is another test post", cover_image="dev/Engineering.png")


with open(PATH_TO_BLOG/"index.html") as index:
    soup = Soup(index.read(), features="html.parser")

#print(str(soup))

write_to_index(path_to_new_post)
update_blog(commit_message="Added another new post")




