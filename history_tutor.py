# Use ChatGTP API to create a history tutoe
######################################### IMPORTS #############################################
import openai
import logging
import os

import tiktoken

from dotenv import load_dotenv

######################################## CONSTANTS ############################################

DATA_DIRECTORY ='data'

########################################### DATA ##############################################

# load environment variables from .env file
load_dotenv()

##################################### HELPER FUCTIONS #########################################

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

# Get the number of tokens in a string
def get_num_tokens_from_string(string, encoding_name="gpt2"):
    tokenizer = tiktoken.get_encoding(encoding_name)
    tokens = tokenizer.encode(string)

    return len(tokens)

######################################## LOGGING ##############################################

logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG) # Supress debugging output from modules imported
#logging.disable(logging.CRITICAL) # Uncomment to disable all logging

######################################### START ###############################################
logging.info('Start of program')

# Get the current DATA directory
home = os.getcwd()
data_dir = os.path.join(home, DATA_DIRECTORY)
logging.info(data_dir)

os.chdir(data_dir)

# Authenticate with OpenAI                             
api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = api_key

########################################## MAIN ###############################################
logging.info('Main section entered')


######################################### FINISH ##############################################
logging.info('End of program')