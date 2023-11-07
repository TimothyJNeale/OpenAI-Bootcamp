import openai
from dotenv import load_dotenv
import os

import requests
import bs4

# load environment variables from .env file
load_dotenv()

################################### Data ####################################

country_newspaper_dict = {"united states": "The New York Times",
                            "united kingdom": "The Guardian",
                            "australia": "The Sydney Morning Herald",
                            "canada": "The Globe and Mail",
                            "india": "The Times of India",
                            "ireland": "The Irish Times",
                            "new zealand": "The New Zealand Herald",
                            "pakistan": "Dawn",
                            "singapore": "The Straits Times",
                            "south africa": "The Mail & Guardian",
                            "spain": "El País",
                            "france": "Le Monde"}
newspaper_url_dict = {"The New York Times": "https://www.nytimes.com/",
                        "The Guardian": "https://www.theguardian.com/international",
                        "The Sydney Morning Herald": "https://www.smh.com.au/",
                        "The Globe and Mail": "https://www.theglobeandmail.com/",
                        "The Times of India": "https://timesofindia.indiatimes.com/",
                        "The Irish Times": "https://www.irishtimes.com/",
                        "The New Zealand Herald": "https://www.nzherald.co.nz/",
                        "Dawn": "https://www.dawn.com/",
                        "The Straits Times": "https://www.straitstimes.com/",
                        "The Mail & Guardian": "https://mg.co.za/",
                        "El País": "https://elpais.com/",
                        "Le Monde": "https://www.lemonde.fr/"}



############################# Helper Functions ###############################

# Use chat completion
def get_chat_completion(prompt, model="gpt-3.5-turbo", temperature=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message["content"]

# Standard completion
def get_completion(prompt, model="gpt-3.5-turbo-instruct", temperature=0, max_tokens=300, stop="\"\"\""):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        stop=stop)

    return response.choices[0].text


############################### Authenticate #################################

# Authenticate with OpenAI                             
api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = api_key


############################### Main Program #################################

country = input("What country are you interested in for news? ")
newspaper = country_newspaper_dict[country.lower()]
url = newspaper_url_dict[newspaper]
print(url)
result = requests.get(url)
print(result.status_code)
soup = bs4.BeautifulSoup(result.text, "html.parser")

print(soup.title.text)
headings = soup.find_all({"h1", "h2", "h3"})
for heading in headings:
    print(heading.text.strip())
