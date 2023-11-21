# Fine tune a model
####################################### IMPORTS ###############################################
import openai
import logging
import os

import pandas as pd

from dotenv import load_dotenv

##################################### CONSTANTS ###############################################

DATA_DIRECTORY ='data'
DATA_FILE = 'python_qa.csv'

# load environment variables from .env file
load_dotenv()

############################################ Data #############################################


################################## HELPER FUCTIONS #############################################

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


####################################### LOGGING ################################################

logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG) # Supress debugging output from modules imported
#logging.disable(logging.CRITICAL) # Uncomment to disable all logging


####################################### START #################################################
logging.info('Start of program')

# Get the current DATA directory
home = os.getcwd()
data_dir = os.path.join(home, DATA_DIRECTORY)
logging.info(data_dir)

os.chdir(data_dir)

# Authenticate with OpenAI                             
api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = api_key

####################################### MAIN ##################################################
# Load the data
input_file = os.path.join(data_dir, DATA_FILE)
logging.info(input_file)
qa_df = pd.read_csv(input_file)
logging.info(qa_df.head())


